"""API de prévision des prix céréaliers (Burkina Faso) — FastAPI.

Lancement : uvicorn app.main:app --host 0.0.0.0 --port 8000
Documentation : http://localhost:8000/docs
"""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field, field_validator

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE / "src"))

from features import PRODUITS, variables_pour_service  # noqa: E402

CHEMIN_MODELES = RACINE / "models" / "registre_modeles.pkl"
CHEMIN_METRIQUES = RACINE / "reports" / "metrics.json"

app = FastAPI(
    title="API Prix des céréales — Burkina Faso",
    description=(
        "Prévision des prix du mil, du maïs et du sorgho sur les marchés burkinabè, "
        "et alerte précoce de flambée des prix.\n\n"
        "Source des données : Programme Alimentaire Mondial (WFP) via HDX.\n\n"
        "⚠️ Service d'aide à la décision : les prévisions à horizon court suivent "
        "la méthode naïve (mesurée comme la plus précise), l'apport du modèle "
        "apparaît à 12 mois. Voir /performance."
    ),
    version="1.0.0",
)

if not CHEMIN_MODELES.exists():
    raise RuntimeError("Registre de modèles introuvable. Lancez : python src/train.py")

PAQUET = joblib.load(CHEMIN_MODELES)
REGISTRE = PAQUET["registre"]
HORIZONS = PAQUET["horizons"]
VARIABLES = PAQUET["variables"]
METRIQUES = (json.loads(CHEMIN_METRIQUES.read_text(encoding="utf-8"))
             if CHEMIN_METRIQUES.exists() else {})
SEUIL_ALERTE = float(REGISTRE["alerte"]["seuil"])


# --------------------------------------------------------------------------- #
# Schémas d'entrée / sortie
# --------------------------------------------------------------------------- #
class PointPrix(BaseModel):
    mois: str = Field(..., description="Mois au format AAAA-MM ou AAAA-MM-JJ")
    prix: float = Field(..., gt=0, le=10000, description="Prix en FCFA/kg")

    @field_validator("mois")
    @classmethod
    def mois_valide(cls, v: str) -> str:
        try:
            pd.Timestamp(v)
        except Exception as exc:  # noqa: BLE001
            raise ValueError(f"mois illisible : {v}") from exc
        return v


class DemandePrevision(BaseModel):
    produit: str = Field(..., description="Millet, Maize (white) ou Sorghum (white)")
    marche: str = Field(..., min_length=2)
    region: str = Field(..., min_length=2)
    historique: list[PointPrix] = Field(
        ..., min_length=13,
        description="Au moins 13 mois consécutifs, du plus ancien au plus récent. "
                    "Le dernier élément = dernier prix connu.")
    prix_national_lag1: float | None = Field(
        None, gt=0, description="Prix national du mois précédent (améliore la précision).")

    @field_validator("produit")
    @classmethod
    def produit_connu(cls, v: str) -> str:
        if v not in PRODUITS:
            raise ValueError(f"produit inconnu. Valeurs acceptées : {PRODUITS}")
        return v

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "produit": "Millet",
                "marche": "Ouahigouya",
                "region": "NORD",
                "prix_national_lag1": 265.0,
                "historique": [{"mois": f"2025-{m:02d}", "prix": 240 + 3 * m}
                               for m in range(1, 13)] + [{"mois": "2026-01", "prix": 279.0}],
            }]
        }
    }


class PrevisionHorizon(BaseModel):
    horizon_mois: int
    mois_prevu: str
    methode_recommandee: str
    valeur_recommandee: float
    prevision_modele: float
    baseline_persistance: float
    ecart_modele_persistance_pct: float


class ReponsePrevision(BaseModel):
    produit: str
    marche: str
    dernier_prix_connu: float
    dernier_mois_connu: str
    previsions: list[PrevisionHorizon]
    avertissement: str


class ReponseAlerte(BaseModel):
    produit: str
    marche: str
    probabilite_flambee: float
    decision: str
    seuil_utilise: float
    performance_modele: dict
    message: str


# --------------------------------------------------------------------------- #
# Utilitaires
# --------------------------------------------------------------------------- #
def _verifier_continuite(historique: list[PointPrix]) -> None:
    """Les décalages n'ont de sens que si les mois se suivent sans trou."""
    ordinaux = pd.to_datetime([p.mois for p in historique]).to_period("M").astype("int64").to_numpy()
    ordinaux.sort()
    ecarts = np.diff(ordinaux)
    if ecarts.size and not (ecarts == 1).all():
        raise HTTPException(
            status_code=422,
            detail="L'historique doit être constitué de mois consécutifs, sans trou "
                   "(les variables de décalage ne seraient pas interprétables).",
        )


def _construire_ligne(demande: DemandePrevision) -> pd.DataFrame:
    _verifier_continuite(demande.historique)
    hist = pd.DataFrame({
        "produit": demande.produit,
        "region": demande.region,
        "marche": demande.marche,
        "mois": pd.to_datetime([p.mois for p in demande.historique]),
        "prix": [p.prix for p in demande.historique],
    }).sort_values("mois")
    try:
        return variables_pour_service(hist, prix_national_lag1=demande.prix_national_lag1)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


def _mois_prevu(dernier_mois: pd.Timestamp, horizon: int) -> str:
    return (pd.Timestamp(dernier_mois) + pd.offsets.MonthBegin(horizon)).strftime("%Y-%m")


# --------------------------------------------------------------------------- #
# Endpoints
# --------------------------------------------------------------------------- #
@app.get("/", include_in_schema=False)
def racine():
    """Redirige vers la documentation interactive (utile pour un aperçu en ligne)."""
    return RedirectResponse(url="/docs")


@app.get("/sante", summary="État du service")
def sante() -> dict:
    return {
        "statut": "ok",
        "modeles_charges": list(REGISTRE),
        "horizons": HORIZONS,
        "source_donnees": "WFP Food Prices — Burkina Faso (HDX, CC-BY-IGO)",
    }


@app.get("/performance", summary="Performance mesurée du modèle (transparence)")
def performance() -> dict:
    """Les chiffres réels, baselines comprises. Un service qui cache ses baselines ment."""
    if not METRIQUES:
        raise HTTPException(status_code=503, detail="Métriques indisponibles.")
    return {"meta": METRIQUES["meta"], "horizons": METRIQUES["horizons"],
            "alerte": METRIQUES["alerte"]}


@app.post("/prevision", response_model=ReponsePrevision, summary="Prévision multi-horizons")
def prevision(demande: DemandePrevision) -> ReponsePrevision:
    ligne = _construire_ligne(demande)
    dernier_prix = float(ligne["prix_lag1"].iloc[0])
    dernier_mois = pd.to_datetime(demande.historique[-1].mois) if len(demande.historique) else None
    dernier_mois = max(pd.to_datetime(p.mois) for p in demande.historique)

    sorties = []
    for h in HORIZONS:
        modele = REGISTRE[f"h{h}"]["modele"]
        delta = float(modele.predict(ligne[VARIABLES])[0])
        prev_modele = dernier_prix + delta
        # la méthode recommandée est celle mesurée comme la meilleure à cet horizon
        meilleure = METRIQUES.get("horizons", {}).get(str(h), {}).get("meilleure_methode", "modele")
        if meilleure == "persistance":
            recommande = dernier_prix
        elif meilleure == "saisonnier_12":
            recommande = float(ligne["prix_lag12"].iloc[0])
        else:
            recommande = prev_modele
        sorties.append(PrevisionHorizon(
            horizon_mois=h,
            mois_prevu=_mois_prevu(dernier_mois, h),
            methode_recommandee=meilleure,
            valeur_recommandee=round(recommande, 1),
            prevision_modele=round(prev_modele, 1),
            baseline_persistance=round(dernier_prix, 1),
            ecart_modele_persistance_pct=round((prev_modele - dernier_prix) / dernier_prix * 100, 1),
        ))

    return ReponsePrevision(
        produit=demande.produit,
        marche=demande.marche,
        dernier_prix_connu=round(dernier_prix, 1),
        dernier_mois_connu=dernier_mois.strftime("%Y-%m"),
        previsions=sorties,
        avertissement=(
            "À 1, 3 et 6 mois, la méthode naïve (dernier prix connu) est mesurée comme la plus "
            "précise sur la période de test : c'est elle qui est recommandée. Le modèle apporte "
            "un gain à 12 mois. Détails chiffrés sur /performance."
        ),
    )


@app.post("/alerte", response_model=ReponseAlerte, summary="Alerte précoce de flambée de prix")
def alerte(demande: DemandePrevision) -> ReponseAlerte:
    ligne = _construire_ligne(demande)
    proba = float(REGISTRE["alerte"]["modele"].predict_proba(ligne[VARIABLES])[0, 1])
    decision = "alerte" if proba >= SEUIL_ALERTE else "vigilance normale"
    return ReponseAlerte(
        produit=demande.produit,
        marche=demande.marche,
        probabilite_flambee=round(proba, 3),
        decision=decision,
        seuil_utilise=SEUIL_ALERTE,
        performance_modele={
            "roc_auc": METRIQUES.get("alerte", {}).get("roc_auc"),
            "pr_auc": METRIQUES.get("alerte", {}).get("pr_auc"),
            "taux_base": METRIQUES.get("alerte", {}).get("taux_base_test"),
            "rappel_au_seuil": METRIQUES.get("alerte", {}).get("rappel"),
            "precision_au_seuil": METRIQUES.get("alerte", {}).get("precision"),
        },
        message=(
            "Probabilité qu'une flambée de +10 % survienne dans les 3 mois. "
            "Le modèle classe 2,3 fois mieux que le hasard : il sert à PRIORISER la "
            "surveillance, pas à décider seul."
        ),
    )

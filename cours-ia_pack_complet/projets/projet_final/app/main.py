"""API de prédiction du risque de défaut — FastAPI.

Lancement : uvicorn app.main:app --host 0.0.0.0 --port 8000
Documentation interactive : http://localhost:8000/docs
"""
from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

RACINE = Path(__file__).resolve().parents[1]
CHEMIN_MODELE = RACINE / "models" / "modele.pkl"
CHEMIN_METRIQUES = RACINE / "reports" / "metrics.json"

app = FastAPI(
    title="API Risque de Défaut — Microfinance",
    description="Prédit la probabilité de défaut de remboursement d'un dossier de crédit.",
    version="1.0.0",
)

if not CHEMIN_MODELE.exists():
    raise RuntimeError("Modèle introuvable. Lancez : python src/train.py")

MODELE = joblib.load(CHEMIN_MODELE)
SEUIL = json.loads(CHEMIN_METRIQUES.read_text(encoding="utf-8"))["seuil"] if CHEMIN_METRIQUES.exists() else 0.5


class DossierCredit(BaseModel):
    """Un dossier de crédit. Les bornes évitent les entrées absurdes."""

    age: int = Field(..., ge=18, le=90, description="Âge du demandeur")
    revenu_mensuel_fcfa: float = Field(..., gt=0, le=10_000_000)
    montant_credit_fcfa: float = Field(..., gt=0, le=100_000_000)
    duree_mois: int = Field(..., ge=1, le=120)
    anciennete_client_mois: int = Field(..., ge=0, le=600)
    nb_credits_precedents: int = Field(..., ge=0, le=50)
    score_mobile_money: float = Field(..., ge=0, le=100)
    secteur: str = Field(..., description="commerce, agriculture, artisanat, elevage, service")
    ville: str = Field(..., description="Ville du demandeur")

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "age": 38, "revenu_mensuel_fcfa": 175000, "montant_credit_fcfa": 500000,
                "duree_mois": 12, "anciennete_client_mois": 30, "nb_credits_precedents": 3,
                "score_mobile_money": 62, "secteur": "commerce", "ville": "Ouagadougou",
            }]
        }
    }


class ReponsePrediction(BaseModel):
    probabilite_defaut: float
    decision: str
    seuil_utilise: float
    message: str


def _features(d: DossierCredit) -> pd.DataFrame:
    """Mêmes variables que celles du pipeline d'entraînement (src/features.py)."""
    ligne = {
        "age": d.age,
        "revenu_mensuel_fcfa": d.revenu_mensuel_fcfa,
        "montant_credit_fcfa": d.montant_credit_fcfa,
        "duree_mois": d.duree_mois,
        "anciennete_client_mois": d.anciennete_client_mois,
        "nb_credits_precedents": d.nb_credits_precedents,
        "score_mobile_money": d.score_mobile_money,
        "secteur": d.secteur.lower().strip(),
        "ville": d.ville.strip(),
    }
    df = pd.DataFrame([ligne])
    df["taux_effort"] = df["montant_credit_fcfa"] / (df["revenu_mensuel_fcfa"] * df["duree_mois"])
    df["credit_par_revenu"] = df["montant_credit_fcfa"] / df["revenu_mensuel_fcfa"]
    df["fidelite"] = df["anciennete_client_mois"] / (df["nb_credits_precedents"] + 1)
    df["jeune_client"] = (df["anciennete_client_mois"] < 12).astype(int)
    df["score_par_age"] = df["score_mobile_money"] / df["age"]
    return df


@app.get("/sante", summary="Vérification de disponibilité")
def sante() -> dict:
    return {"statut": "ok", "modele_charge": True, "seuil": SEUIL}


@app.post("/predire", response_model=ReponsePrediction, summary="Prédire le risque de défaut")
def predire(dossier: DossierCredit) -> ReponsePrediction:
    try:
        proba = float(MODELE.predict_proba(_features(dossier))[0, 1])
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=f"Erreur de prédiction : {exc}") from exc

    decision = "refus" if proba >= SEUIL else "accord"
    message = (
        "Risque élevé : étude manuelle recommandée." if decision == "refus"
        else "Risque dans les limites acceptées par le modèle."
    )
    return ReponsePrediction(
        probabilite_defaut=round(proba, 4),
        decision=decision,
        seuil_utilise=SEUIL,
        message=message,
    )

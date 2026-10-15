"""Interface Streamlit — démonstration publique de l'API de prévision.

Lancement : streamlit run app/ui.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE / "src"))
from features import PRODUITS, variables_pour_service  # noqa: E402

PAQUET = joblib.load(RACINE / "models" / "registre_modeles.pkl")
REGISTRE, HORIZONS, VARIABLES = PAQUET["registre"], PAQUET["horizons"], PAQUET["variables"]
METRIQUES = json.loads((RACINE / "reports" / "metrics.json").read_text(encoding="utf-8"))

st.set_page_config(page_title="Prix des céréales — Burkina Faso", page_icon="🌾", layout="wide")
st.title("🌾 Prévision des prix céréaliers — Burkina Faso")
st.caption("Données réelles du Programme Alimentaire Mondial (WFP/HDX, 2016-2026) · mil, maïs, sorgho · 64 marchés")

onglet_prev, onglet_alerte, onglet_perf = st.tabs(["📈 Prévision", "🚨 Alerte de flambée", "📊 Performance du modèle"])

with st.sidebar:
    st.header("Votre marché")
    produit = st.selectbox("Produit", PRODUITS, index=1)
    marche = st.text_input("Marché", "Ouahigouya")
    region = st.text_input("Région", "NORD")
    st.divider()
    st.subheader("Historique des prix (FCFA/kg)")
    st.caption("Le dernier mois saisi = dernier prix connu. 13 mois minimum.")

    import numpy as np
    rng = np.random.default_rng(3)
    defaut = pd.DataFrame({
        "mois": pd.date_range("2025-01-01", periods=13, freq="MS"),
        "prix": [248, 252, 261, 274, 288, 301, 312, 305, 289, 276, 268, 271, 279],
    })
    edite = st.data_editor(defaut, num_rows="dynamic", height=330,
                           column_config={"mois": st.column_config.DateColumn("Mois", format="YYYY-MM"),
                                          "prix": st.column_config.NumberColumn("Prix FCFA/kg", min_value=30)})

if edite is None or len(edite) < 13:
    st.warning("Saisissez au moins 13 mois d'historique.")
    st.stop()

hist = pd.DataFrame({
    "produit": produit, "region": region, "marche": marche,
    "mois": pd.to_datetime(edite["mois"]), "prix": edite["prix"].astype(float),
}).dropna().sort_values("mois")

try:
    ligne = variables_pour_service(hist)
except ValueError as exc:
    st.error(f"Impossible de calculer les variables : {exc}")
    st.stop()

dernier_prix = float(ligne["prix_lag1"].iloc[0])
dernier_mois = hist["mois"].iloc[-1]
st.info(f"Dernier prix connu : **{dernier_prix:.0f} FCFA/kg** ({dernier_mois:%m/%Y}) — {produit}, {marche}")

# ---------------- Prévision ----------------
with onglet_prev:
    st.subheader("Prévisions par horizon")
    lignes = []
    for h in HORIZONS:
        modele = REGISTRE[f"h{h}"]["modele"]
        prev_modele = dernier_prix + float(modele.predict(ligne[VARIABLES])[0])
        meilleure = METRIQUES["horizons"][str(h)]["meilleure_methode"]
        recommande = (dernier_prix if meilleure == "persistance"
                      else float(ligne["prix_lag12"].iloc[0]) if meilleure == "saisonnier_12"
                      else prev_modele)
        lignes.append({
            "Horizon": f"{h} mois", "Mois prévu": (dernier_mois + pd.offsets.MonthBegin(h)).strftime("%Y-%m"),
            "Méthode recommandée": {"persistance": "prix du dernier mois", "modele": "modèle ML",
                                    "saisonnier_12": "même mois, année précédente"}[meilleure],
            "Valeur prévue": round(recommande),
            "Modèle ML": round(prev_modele),
            "Écart vs dernier prix": f"{(prev_modele - dernier_prix) / dernier_prix * 100:+.1f} %",
        })
    tableau = pd.DataFrame(lignes)
    st.dataframe(tableau, use_container_width=True, hide_index=True)
    c1, c2, c3, c4 = st.columns(4)
    for col, h in zip((c1, c2, c3, c4), HORIZONS):
        col.metric(f"Dans {h} mois", f"{tableau.loc[tableau['Horizon'] == f'{h} mois', 'Valeur prévue'].iloc[0]:.0f} FCFA",
                   help="Méthode recommandée d'après la performance mesurée")
    st.warning("**Honnêteté du résultat :** à 1, 3 et 6 mois, la méthode naïve reste la plus précise "
               "sur la période de test. Le modèle ML n'apporte un gain qu'à 12 mois — c'est écrit dans "
               "l'onglet Performance, baselines comprises.")

# ---------------- Alerte ----------------
with onglet_alerte:
    proba = float(REGISTRE["alerte"]["modele"].predict_proba(ligne[VARIABLES])[0, 1])
    seuil = float(REGISTRE["alerte"]["seuil"])
    st.subheader("Risque de flambée : +10 % en 3 mois")
    c1, c2 = st.columns([1, 2])
    c1.metric("Probabilité", f"{proba:.0%}")
    if proba >= seuil:
        c2.error(f"🚨 **Alerte** (seuil {seuil}) — surveillance renforcée recommandée.")
    else:
        c2.success(f"✅ Sous le seuil d'alerte ({seuil}).")
    st.progress(min(proba, 1.0))
    a = METRIQUES["alerte"]
    st.markdown(f"""
**Ce que ce score vaut réellement (mesuré sur 2025-2026) :**
- ROC-AUC **{a['roc_auc']}** · PR-AUC **{a['pr_auc']}** contre un taux de base de **{a['taux_base_test']}** → **{a['pr_auc']/a['taux_base_test']:.1f}× mieux que le hasard**
- Au seuil {a['seuil']} : **{a['rappel']:.0%} des flambées détectées**, {a['precision']:.0%} de précision, {a['taux_alerte']:.0%} des mois signalés
- Usage prévu : **prioriser la surveillance** des marchés, pas décider seul d'une intervention
""")

# ---------------- Performance ----------------
with onglet_perf:
    st.subheader("Comparaison aux baselines naïves (test 2025-2026)")
    lignes = []
    for h in HORIZONS:
        m = METRIQUES["horizons"][str(h)]["methodes"]
        lignes.append({
            "Horizon": f"{h} mois",
            "Persistance (MAE)": m["persistance"]["MAE"],
            "Saisonnier -12 (MAE)": m["saisonnier_12"]["MAE"],
            "Modèle ML (MAE)": m["modele"]["MAE"],
            "Meilleure méthode": METRIQUES["horizons"][str(h)]["meilleure_methode"],
        })
    st.dataframe(pd.DataFrame(lignes), use_container_width=True, hide_index=True)
    st.caption("MAE en FCFA/kg — plus petit = meilleur. "
               "La leçon principale : sur des prix alimentaires, la marche aléatoire est un adversaire redoutable. "
               "Un projet honnête le dit ; un projet qui l'ignore n'a pas de valeur en production.")
    st.image(str(RACINE / "reports" / "figures" / "prevision_12_mois.png"),
             caption="Prévision à 12 mois — modèle contre baseline")

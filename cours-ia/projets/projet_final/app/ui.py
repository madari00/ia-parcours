"""Interface Streamlit — démonstration publique du modèle.

Lancement : streamlit run app/ui.py
"""
from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

RACINE = Path(__file__).resolve().parents[1]
MODELE = joblib.load(RACINE / "models" / "modele.pkl")
SEUIL = json.loads((RACINE / "reports" / "metrics.json").read_text(encoding="utf-8"))["seuil"]

st.set_page_config(page_title="Risque de défaut — Microfinance", page_icon="📊")
st.title("📊 Prédiction du risque de défaut")
st.caption("Microfinance · Burkina Faso — modèle d'aide à la décision (le conseiller garde la décision finale)")

col1, col2 = st.columns(2)
with col1:
    age = st.slider("Âge", 18, 90, 38)
    revenu = st.number_input("Revenu mensuel (FCFA)", 20_000, 5_000_000, 175_000, step=5_000)
    montant = st.number_input("Montant du crédit (FCFA)", 50_000, 20_000_000, 500_000, step=50_000)
    duree = st.selectbox("Durée (mois)", [6, 12, 18, 24, 36], index=1)
with col2:
    anciennete = st.slider("Ancienneté client (mois)", 0, 240, 30)
    nb_credits = st.slider("Crédits antérieurs", 0, 10, 3)
    score_mm = st.slider("Score Mobile Money (0-100)", 0, 100, 62)
    secteur = st.selectbox("Secteur", ["commerce", "agriculture", "artisanat", "elevage", "service"])
    ville = st.selectbox("Ville", ["Ouagadougou", "Bobo-Dioulasso", "Koudougou", "Ouahigouya", "Banfora"])

if st.button("Évaluer le dossier", type="primary"):
    ligne = pd.DataFrame([{
        "age": age, "revenu_mensuel_fcfa": revenu, "montant_credit_fcfa": montant,
        "duree_mois": duree, "anciennete_client_mois": anciennete,
        "nb_credits_precedents": nb_credits, "score_mobile_money": score_mm,
        "secteur": secteur, "ville": ville,
    }])
    ligne["taux_effort"] = montant / (revenu * duree)
    ligne["credit_par_revenu"] = montant / revenu
    ligne["fidelite"] = anciennete / (nb_credits + 1)
    ligne["jeune_client"] = int(anciennete < 12)
    ligne["score_par_age"] = score_mm / age

    proba = float(MODELE.predict_proba(ligne)[0, 1])
    st.metric("Probabilité de défaut", f"{proba:.1%}")
    st.progress(min(proba, 1.0))
    if proba >= SEUIL:
        st.error(f"⚠️ Risque élevé (seuil {SEUIL}) — étude manuelle recommandée.")
    else:
        st.success(f"✅ Risque acceptable (seuil {SEUIL}).")

st.divider()
st.caption(
    "Modèle d'aide à la décision. Il ne remplace pas l'analyse du conseiller : "
    "chaque refus doit pouvoir être expliqué au client (RGPD, droit à l'explication)."
)

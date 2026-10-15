"""Préparation des variables : nettoyage, colonnes numériques/catégorielles, features."""
from __future__ import annotations

import pandas as pd

COLS_NUM = [
    "age",
    "revenu_mensuel_fcfa",
    "montant_credit_fcfa",
    "duree_mois",
    "anciennete_client_mois",
    "nb_credits_precedents",
    "score_mobile_money",
]
COLS_CAT = ["secteur", "ville"]


def nettoyer(df: pd.DataFrame) -> pd.DataFrame:
    """Nettoyage minimal : doublons, valeurs impossibles, types."""
    df = df.copy()
    df = df.drop_duplicates()

    # Valeurs impossibles -> NaN (elles seront imputées par le pipeline)
    df.loc[df["age"] < 18, "age"] = pd.NA
    df.loc[df["age"] > 90, "age"] = pd.NA
    df.loc[df["revenu_mensuel_fcfa"] <= 0, "revenu_mensuel_fcfa"] = pd.NA
    df.loc[df["montant_credit_fcfa"] <= 0, "montant_credit_fcfa"] = pd.NA

    df["secteur"] = df["secteur"].astype("string").str.lower().str.strip()
    df["ville"] = df["ville"].astype("string").str.strip()
    return df


def ajouter_features(df: pd.DataFrame) -> pd.DataFrame:
    """Ingénierie de variables : ratios et croisements utiles au métier."""
    df = df.copy()
    df["taux_effort"] = df["montant_credit_fcfa"] / (df["revenu_mensuel_fcfa"] * df["duree_mois"])
    df["credit_par_revenu"] = df["montant_credit_fcfa"] / df["revenu_mensuel_fcfa"]
    df["fidelite"] = df["anciennete_client_mois"] / (df["nb_credits_precedents"] + 1)
    df["jeune_client"] = (df["anciennete_client_mois"] < 12).astype(int)
    df["score_par_age"] = df["score_mobile_money"] / df["age"]
    return df


COLS_NUM_FINAL = COLS_NUM + [
    "taux_effort",
    "credit_par_revenu",
    "fidelite",
    "jeune_client",
    "score_par_age",
]


def preparer(df: pd.DataFrame) -> pd.DataFrame:
    """Pipeline de préparation complet (nettoyage + features)."""
    return ajouter_features(nettoyer(df))

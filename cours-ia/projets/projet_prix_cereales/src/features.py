"""Construction des variables — utilisée À LA FOIS par l'entraînement et l'API.

Principe de fer : **toute variable doit être calculable avec les données ≤ t-1.**
C'est ce qui empêche la fuite temporelle et garantit qu'il n'y a pas d'écart
entre l'entraînement et la mise en service (train/serve skew).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

PRODUITS = ["Maize (white)", "Millet", "Sorghum (white)"]

VARIABLES_NUM = [
    "prix_lag1", "prix_lag2", "prix_lag3", "prix_lag6", "prix_lag12",
    "moyenne_mobile3", "moyenne_mobile6", "moyenne_mobile12",
    "ecart_moyenne12", "prix_national_lag1", "ratio_national", "mois_num",
    "d1", "d2", "d3", "d6", "d12", "ratio_lag1_lag12", "volatilite6",
]
VARIABLES_CAT = ["produit", "region", "marche"]
VARIABLES = VARIABLES_NUM + VARIABLES_CAT

MOIS_HISTORIQUE_REQUIS = 13      # il faut 12 mois de recul pour prix_lag12


def construire_variables(df: pd.DataFrame, national: pd.DataFrame | None = None) -> pd.DataFrame:
    """Ajoute les variables explicatives à un panneau [produit, region, marche, mois, prix].

    Arguments
    ---------
    df : historique long, trié ou non, avec au moins les colonnes
         produit, region, marche, mois, prix.
    national : table optionnelle [produit, mois, prix_national] pour le prix
         national de référence. À l'entraînement, elle est calculée sur tout le
         panneau (moyenne inter-marchés). En service, on la fournit ou l'on
         retombe sur le prix local.

    Toutes les variables sont décalées : elles n'utilisent que le passé.
    """
    df = df.copy()
    df["mois"] = pd.to_datetime(df["mois"])
    df = df.sort_values(["produit", "marche", "mois"]).reset_index(drop=True)
    g = df.groupby(["produit", "marche"], observed=True)

    # Historique de prix (décalages)
    for k in (1, 2, 3, 6, 12):
        df[f"prix_lag{k}"] = g["prix"].shift(k)

    # Moyennes mobiles : décalées de 1 mois pour ne pas inclure le mois courant
    for f in (3, 6, 12):
        df[f"moyenne_mobile{f}"] = g["prix"].transform(
            lambda s, f=f: s.shift(1).rolling(f, min_periods=f).mean()
        )

    # Écarts et tendances (toujours sur des prix passés)
    df["ecart_moyenne12"] = df["prix_lag1"] - df["moyenne_mobile12"]
    df["d1"] = df["prix_lag1"] - df["prix_lag2"]
    df["d2"] = df["prix_lag2"] - df["prix_lag3"]
    df["d3"] = df["prix_lag1"] - df["prix_lag3"]
    df["d6"] = df["prix_lag1"] - df["prix_lag6"]
    df["d12"] = df["prix_lag1"] - df["prix_lag12"]
    df["ratio_lag1_lag12"] = df["prix_lag1"] / df["prix_lag12"]
    df["volatilite6"] = g["prix"].transform(
        lambda s: s.shift(1).rolling(6, min_periods=6).std()
    )

    # Prix national de référence, décalé d'un mois
    if national is None:
        national = (df.groupby(["produit", "mois"], as_index=False, observed=True)["prix"].mean()
                      .rename(columns={"prix": "prix_national"}))
    nationale = national.copy()
    nationale["mois"] = pd.to_datetime(nationale["mois"])
    nationale = nationale.sort_values(["produit", "mois"])
    nationale["prix_national_lag1"] = (nationale.groupby("produit", observed=True)["prix_national"]
                                               .shift(1))
    df = df.merge(nationale[["produit", "mois", "prix_national_lag1"]],
                  on=["produit", "mois"], how="left")
    # Filet de sécurité en service : si le prix national est inconnu, on utilise le prix local
    df["prix_national_lag1"] = df["prix_national_lag1"].fillna(df["prix_lag1"])
    df["ratio_national"] = df["prix_lag1"] / df["prix_national_lag1"]

    # Calendrier
    df["annee"] = df["mois"].dt.year
    df["mois_num"] = df["mois"].dt.month

    # Catégorielles
    for c in VARIABLES_CAT:
        df[c] = df[c].astype("category")
    return df


def historique_complet(df: pd.DataFrame) -> pd.DataFrame:
    """Garde uniquement les lignes exploitables (historique suffisant, prix plausible)."""
    df = df[df["prix"].between(30, 3000)]
    return df.dropna(subset=["prix_lag12", "moyenne_mobile12", "volatilite6",
                             "prix_national_lag1"]).reset_index(drop=True)


def variables_pour_service(historique: pd.DataFrame,
                           prix_national_lag1: float | None = None) -> pd.DataFrame:
    """Prépare la ligne de variables pour UNE série, prête à être servie par l'API.

    `historique` : DataFrame [produit, region, marche, mois, prix] couvrant au
    moins 13 mois consécutifs ; le DERNIER mois est le dernier prix connu.

    On ajoute une ligne « mois suivant » (prix inconnu, donc NaN) : les variables
    de cette ligne n'utilisent que les prix réellement connus, ce qui reproduit
    exactement la situation de la prévision en production.
    """
    if len(historique) < MOIS_HISTORIQUE_REQUIS:
        raise ValueError(
            f"Historique insuffisant : {len(historique)} mois fournis, "
            f"{MOIS_HISTORIQUE_REQUIS} requis."
        )
    interdits = {"prix_lag1", "mois_num", "d1", "moyenne_mobile3"} & set(historique.columns)
    if interdits:
        raise ValueError(f"Colonnes déjà calculées reçues en entrée (risque de fuite) : {interdits}")

    hist = historique.sort_values("mois").copy()
    dernier = hist.iloc[-1]
    suivant = {"produit": dernier["produit"], "region": dernier["region"],
               "marche": dernier["marche"],
               "mois": pd.to_datetime(dernier["mois"]) + pd.offsets.MonthBegin(1),
               "prix": np.nan}
    etendu = pd.concat([hist, pd.DataFrame([suivant])], ignore_index=True)

    v = construire_variables(etendu)
    if prix_national_lag1 is not None:
        v["prix_national_lag1"] = float(prix_national_lag1)
        v["ratio_national"] = v["prix_lag1"] / v["prix_national_lag1"]

    derniere = v.iloc[[-1]]
    manquantes = [c for c in VARIABLES_NUM if pd.isna(derniere[c].iloc[0])]
    if manquantes:
        raise ValueError(f"Variables indisponibles : {manquantes} "
                         "(fournir un historique plus long ou plus régulier)")
    return derniere


def serie_modele() -> list[str]:
    """Ordre des colonnes attendu par les modèles."""
    return VARIABLES

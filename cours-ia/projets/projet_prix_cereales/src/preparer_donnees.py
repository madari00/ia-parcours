"""Préparation des données réelles : prix des céréales au Burkina Faso (source WFP/HDX).

Entrée  : data/raw/wfp_food_prices_bfa.csv   (données brutes du Programme Alimentaire Mondial)
Sortie  : data/processed/prix_mensuels.csv   (panneau mensuel par produit × marché)

Source : World Food Programme — Food Prices for Burkina Faso
         https://data.humdata.org/dataset/wfp-food-prices-for-burkina-faso
Licence : Creative Commons Attribution for Intergovernmental Organisations (CC-BY-IGO)

Usage : python src/preparer_donnees.py
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

RACINE = Path(__file__).resolve().parents[1]

PRODUITS = ["Maize (white)", "Millet", "Sorghum (white)"]
DEBUT = "2014-01-01"          # fenêtre récente : régime de prix homogène
MIN_MOIS_SERIE = 48           # au moins 4 ans d'historique par série
INTERPOLATION_MAX = 2         # trous de 1-2 mois comblés, au-delà la série est coupée


def charger_brut(chemin: Path | None = None) -> pd.DataFrame:
    chemin = chemin or RACINE / "data" / "raw" / "wfp_food_prices_bfa.csv"
    if not chemin.exists():
        raise SystemExit(
            "❌ Données brutes absentes.\n"
            "   Télécharge le CSV depuis :\n"
            "   https://data.humdata.org/dataset/wfp-food-prices-for-burkina-faso\n"
            f"   puis place-le ici : {chemin}"
        )
    df = pd.read_csv(chemin, parse_dates=["date"])
    print(f"📥 {len(df):,} lignes brutes chargées".replace(",", " "))
    return df


def filtrer_et_agreger(df: pd.DataFrame) -> pd.DataFrame:
    """Garde les céréales de base, ventes au détail, prix réels, en FCFA/kg."""
    avant = len(df)
    df = df[
        (df["commodity"].isin(PRODUITS))
        & (df["pricetype"] == "Retail")
        & (df["priceflag"] == "actual")
        & (df["unit"] == "KG")
        & (df["currency"] == "XOF")
        & (df["date"] >= DEBUT)
        & (df["price"] > 0)
    ].copy()
    print(f"🧹 filtrage : {avant:,} → {len(df):,} lignes".replace(",", " "))

    df["mois"] = df["date"].values.astype("datetime64[M]")
    groupe = df.groupby(["commodity", "admin1", "market", "mois"], as_index=False).agg(
        prix=("price", "median"),          # médiane : robuste aux valeurs extrêmes
        n_obs=("price", "size"),
    )
    return groupe


def construire_panneau(groupe: pd.DataFrame) -> pd.DataFrame:
    """Grille mensuelle complète par série (produit × marché), avec trous comblés."""
    mois_min, mois_max = groupe["mois"].min(), groupe["mois"].max()
    grille = pd.date_range(mois_min, mois_max, freq="MS")
    series, imputes = [], []

    for (produit, admin1, marche), bloc in groupe.groupby(["commodity", "admin1", "market"]):
        s = bloc.set_index("mois")["prix"].reindex(grille)
        if s.notna().sum() < MIN_MOIS_SERIE:
            continue
        s_imp = s.interpolate(method="linear", limit=INTERPOLATION_MAX,
                              limit_area="inside").ffill().bfill()
        # on coupe les bords non observés
        premiers = s_imp.first_valid_index()
        derniers = s_imp.last_valid_index()
        s_imp = s_imp.loc[premiers:derniers]
        n_imputes = int(s_imp.notna().sum() - s.reindex(s_imp.index).notna().sum())
        series.append(pd.DataFrame({
            "produit": produit, "region": admin1, "marche": marche,
            "mois": s_imp.index, "prix": s_imp.to_numpy(),
        }))
        imputes.append(n_imputes)

    panneau = pd.concat(series, ignore_index=True).sort_values(
        ["produit", "marche", "mois"]).reset_index(drop=True)
    print(f"✅ {panneau['marche'].nunique()} marchés × {panneau['produit'].nunique()} produits "
          f"| {len(panneau):,} observations mensuelles".replace(",", " "))
    print(f"   valeurs interpolées : {sum(imputes):,}".replace(",", " "))
    return panneau


def ajouter_colonnes_reference(panneau: pd.DataFrame) -> pd.DataFrame:
    """Variables calculables sans aucune fuite : elles n'utilisent que le passé."""
    panneau = panneau.sort_values(["produit", "marche", "mois"]).copy()
    g = panneau.groupby(["produit", "marche"], group_keys=False)

    for k in (1, 2, 3, 6, 12):
        panneau[f"prix_lag{k}"] = g["prix"].shift(k)
    for f in (3, 6, 12):
        # transform = calcul par série (aucun mélange entre marchés), décalé de 1 mois
        panneau[f"moyenne_mobile{f}"] = g["prix"].transform(
            lambda s, f=f: s.shift(1).rolling(f, min_periods=f).mean()
        )
    panneau["ecart_moyenne12"] = panneau["prix_lag1"] - panneau["moyenne_mobile12"]
    panneau["tendance"] = panneau["prix_lag1"] - panneau["prix_lag3"]

    # Prix national du produit, décalé d'un mois (connu au moment de la prévision)
    national = (panneau.groupby(["produit", "mois"], as_index=False)["prix"].mean()
                        .rename(columns={"prix": "prix_national"}))
    national["prix_national_lag1"] = national.groupby("produit")["prix_national"].shift(1)
    panneau = panneau.merge(national[["produit", "mois", "prix_national_lag1"]],
                            on=["produit", "mois"], how="left")
    panneau["ratio_national"] = panneau["prix_lag1"] / panneau["prix_national_lag1"]

    # Calendrier
    panneau["annee"] = panneau["mois"].dt.year
    panneau["mois_num"] = panneau["mois"].dt.month
    mois_depuis_debut = (panneau["mois"].dt.year - panneau["mois"].dt.year.min()) * 12 + panneau["mois"].dt.month
    panneau["temps"] = mois_depuis_debut
    return panneau


def main() -> None:
    df = charger_brut()
    groupe = filtrer_et_agreger(df)
    panneau = construire_panneau(groupe)
    panneau = ajouter_colonnes_reference(panneau)

    # Nettoyage final : valeurs aberrantes et lignes inexploitables
    panneau = panneau[panneau["prix"].between(30, 3000)]          # FCFA/kg plausibles
    avant = len(panneau)
    panneau = panneau.dropna(subset=["prix_lag12", "moyenne_mobile12"])
    print(f"🔎 lignes supprimées (valeurs extrêmes ou historique insuffisant) : {avant - len(panneau):,}".replace(",", " "))

    sortie = RACINE / "data" / "processed" / "prix_mensuels.csv"
    sortie.parent.mkdir(parents=True, exist_ok=True)
    panneau.to_csv(sortie, index=False)
    print(f"\n💾 écrit : {sortie}")
    print(f"   {len(panneau):,} lignes | période : {panneau['mois'].min():%Y-%m} → {panneau['mois'].max():%Y-%m}".replace(",", " "))
    print(panneau.groupby("produit")["prix"].agg(["count", "mean", "median"]).round(1).to_string())


if __name__ == "__main__":
    main()

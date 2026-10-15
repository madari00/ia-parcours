"""Génération de données simulées réalistes pour le projet de prédiction de défaut.

⚠️ À remplacer par de vraies données anonymisées quand tu en auras.
Ce script permet de tester tout le pipeline hors ligne, sans dépendance externe.
"""
from pathlib import Path

import numpy as np
import pandas as pd

SECTEURS = ["commerce", "agriculture", "artisanat", "elevage", "service"]
VILLES = ["Ouagadougou", "Bobo-Dioulasso", "Koudougou", "Ouahigouya", "Banfora"]
POIDS_VILLES = [0.42, 0.24, 0.13, 0.11, 0.10]


def generer(n: int = 6000, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    age = rng.integers(21, 68, n)
    secteur = rng.choice(SECTEURS, n, p=[0.4, 0.25, 0.15, 0.12, 0.08])
    ville = rng.choice(VILLES, n, p=POIDS_VILLES)

    # Revenu mensuel : plus élevé en ville et dans le commerce/service
    base_revenu = np.where(ville == "Ouagadougou", 1.35, 1.0)
    base_revenu *= np.where(np.isin(secteur, ["commerce", "service"]), 1.3, 0.85)
    revenu = (rng.lognormal(mean=11.2, sigma=0.45, size=n) * base_revenu).round(-3)

    montant_credit = (revenu * rng.uniform(1.5, 6.0, n)).round(-4)
    duree_mois = rng.choice([6, 12, 18, 24, 36], n, p=[0.15, 0.4, 0.2, 0.15, 0.10])
    anciennete = rng.integers(0, 121, n)
    nb_credits = rng.integers(0, 8, n)
    score_mm = np.clip(rng.normal(55, 18, n), 0, 100).round(0)

    # Score latent de défaut (structure réaliste et bruitée)
    logit = (
        -1.15
        - 0.021 * (age - 40)
        - 0.0000035 * revenu
        + 0.0000028 * montant_credit
        + 0.028 * (duree_mois - 12)
        - 0.010 * anciennete
        - 0.22 * nb_credits
        - 0.033 * (score_mm - 55)
        + 0.35 * (secteur == "agriculture")   # saisonnalité, aléas climatiques
        + rng.normal(0, 0.85, n)              # bruit : une partie est imprévisible
    )
    proba = 1 / (1 + np.exp(-logit))
    defaut = (rng.random(n) < proba).astype(int)

    df = pd.DataFrame({
        "age": age,
        "revenu_mensuel_fcfa": revenu.astype(int),
        "montant_credit_fcfa": montant_credit.astype(int),
        "duree_mois": duree_mois,
        "anciennete_client_mois": anciennete,
        "nb_credits_precedents": nb_credits,
        "score_mobile_money": score_mm.astype(int),
        "secteur": secteur,
        "ville": ville,
        "defaut": defaut,
    })

    # On simule un peu de monde réel : valeurs manquantes et doublons
    for col in ["revenu_mensuel_fcfa", "score_mobile_money"]:
        idx = rng.choice(n, size=int(0.02 * n), replace=False)
        df.loc[idx, col] = np.nan
    df = pd.concat([df, df.sample(20, random_state=seed)], ignore_index=True)

    return df


def main() -> None:
    racine = Path(__file__).resolve().parents[1]
    dossier = racine / "data" / "raw"
    dossier.mkdir(parents=True, exist_ok=True)
    chemin = dossier / "dossiers_credit.csv"
    df = generer()
    df.to_csv(chemin, index=False)
    print(f"✅ {len(df)} dossiers écrits dans {chemin}")
    print(f"Taux de défaut : {df['defaut'].mean():.1%}")


if __name__ == "__main__":
    main()

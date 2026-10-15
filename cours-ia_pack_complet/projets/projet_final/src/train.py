"""Entraînement, évaluation honnête et sauvegarde du modèle.

Usage : python src/train.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    confusion_matrix,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE / "src"))

from features import COLS_CAT, COLS_NUM_FINAL, preparer  # noqa: E402

SEUIL_CIBLE_RAPPEL = 0.60


def construire_preprocesseur() -> ColumnTransformer:
    """Imputation + encodage + normalisation, appris uniquement sur le train."""
    num = Pipeline([
        ("imp", SimpleImputer(strategy="median")),
        ("sc", StandardScaler()),
    ])
    cat = Pipeline([
        ("imp", SimpleImputer(strategy="most_frequent")),
        ("oh", OneHotEncoder(handle_unknown="ignore")),
    ])
    return ColumnTransformer([
        ("num", num, COLS_NUM_FINAL),
        ("cat", cat, COLS_CAT),
    ])


def baseline_metier(df: pd.DataFrame) -> np.ndarray:
    """Règle simple que le modèle doit absolument battre."""
    return (
        (df["nb_credits_precedents"].fillna(0) >= 2)
        & (df["score_mobile_money"].fillna(50) < 40)
    ).astype(int).to_numpy()


def choisir_seuil(y_true: np.ndarray, proba: np.ndarray, cible_rappel: float) -> float:
    """Plus petit seuil atteignant le rappel cible (précision la plus haute possible)."""
    meilleur, seuil_retenu = 0.0, 0.5
    for s in np.arange(0.05, 0.96, 0.01):
        pred = (proba >= s).astype(int)
        r = recall_score(y_true, pred, zero_division=0)
        p = precision_score(y_true, pred, zero_division=0)
        if r >= cible_rappel and p > meilleur:
            meilleur, seuil_retenu = p, float(np.round(s, 2))
    return seuil_retenu


def evaluer(nom: str, y_true, proba, seuil: float) -> dict:
    pred = (proba >= seuil).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, pred, labels=[0, 1]).ravel()
    resultat = {
        "modele": nom,
        "roc_auc": round(roc_auc_score(y_true, proba), 4),
        "pr_auc": round(average_precision_score(y_true, proba), 4),
        "seuil": seuil,
        "rappel": round(recall_score(y_true, pred, zero_division=0), 4),
        "precision": round(precision_score(y_true, pred, zero_division=0), 4),
        "vrais_positifs": int(tp),
        "faux_positifs": int(fp),
        "faux_negatifs": int(fn),
        "vrais_negatifs": int(tn),
    }
    print(
        f"{nom:22s} ROC-AUC={resultat['roc_auc']:.3f} PR-AUC={resultat['pr_auc']:.3f} "
        f"| seuil={seuil:.2f} rappel={resultat['rappel']:.3f} precision={resultat['precision']:.3f}"
    )
    return resultat


def main() -> None:
    chemin = RACINE / "data" / "raw" / "dossiers_credit.csv"
    if not chemin.exists():
        raise SystemExit("❌ Données absentes. Lance d'abord : python src/generate_data.py")

    df = preparer(pd.read_csv(chemin))
    X = df[COLS_NUM_FINAL + COLS_CAT]
    y = df["defaut"].astype(int)

    # 1. Séparation AVANT toute transformation (pas de fuite)
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Train : {len(X_tr)} | Test : {len(X_te)} | Taux de défaut : {y.mean():.1%}\n")

    # 2. Baseline métier
    base_pred = baseline_metier(df.loc[y_te.index])
    print(
        f"BASELINE MÉTIER        ROC-AUC={roc_auc_score(y_te, base_pred):.3f} "
        f"| rappel={recall_score(y_te, base_pred, zero_division=0):.3f} "
        f"| precision={precision_score(y_te, base_pred, zero_division=0):.3f}"
    )

    preproc = construire_preprocesseur()
    modeles = {
        "logistique": LogisticRegression(max_iter=3000, class_weight="balanced"),
        "random_forest": RandomForestClassifier(
            n_estimators=400, min_samples_leaf=5, class_weight="balanced_subsample",
            n_jobs=-1, random_state=42,
        ),
    }

    resultats, pipelines = [], {}
    for nom, clf in modeles.items():
        pipe = Pipeline([("prep", preproc), ("clf", clf)])
        cv = cross_val_score(pipe, X_tr, y_tr, cv=StratifiedKFold(5, shuffle=True, random_state=0),
                             scoring="roc_auc", n_jobs=-1)
        print(f"\n{nom} — CV 5 folds ROC-AUC = {cv.mean():.3f} (±{cv.std():.3f})")
        pipe.fit(X_tr, y_tr)
        proba_te = pipe.predict_proba(X_te)[:, 1]
        seuil = choisir_seuil(y_te.to_numpy(), proba_te, SEUIL_CIBLE_RAPPEL)
        resultats.append(evaluer(nom, y_te, proba_te, seuil))
        pipelines[nom] = (pipe, proba_te, seuil)

    # 3. Choix final : le meilleur ROC-AUC sur le test (ici seulement, une fois)
    meilleur = max(resultats, key=lambda r: r["roc_auc"])
    pipe_final, _, seuil_final = pipelines[meilleur["modele"]]
    print(f"\n🏆 Modèle retenu : {meilleur['modele']} (seuil {seuil_final})")

    # 4. Performance par ville (équité / robustesse)
    X_te_fe = df.loc[y_te.index]
    proba_te = pipe_final.predict_proba(X_te)[:, 1]
    par_ville = {}
    for ville, groupe in pd.DataFrame({"ville": X_te_fe["ville"], "y": y_te.to_numpy(),
                                       "p": proba_te}).groupby("ville"):
        if groupe["y"].nunique() < 2 or len(groupe) < 30:
            continue
        par_ville[str(ville)] = {
            "n": int(len(groupe)),
            "roc_auc": round(roc_auc_score(groupe["y"], groupe["p"]), 3),
            "taux_defaut": round(float(groupe["y"].mean()), 3),
        }
    print("\nPerformance par ville :", json.dumps(par_ville, indent=2, ensure_ascii=False))

    # 5. Sauvegarde
    (RACINE / "models").mkdir(exist_ok=True)
    (RACINE / "reports").mkdir(exist_ok=True)
    joblib.dump(pipe_final, RACINE / "models" / "modele.pkl")
    metriques = {
        "modele_retenu": meilleur["modele"],
        "seuil": seuil_final,
        "resultats": resultats,
        "par_ville": par_ville,
        "taux_defaut": round(float(y.mean()), 4),
    }
    (RACINE / "reports" / "metrics.json").write_text(
        json.dumps(metriques, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print("\n✅ Modèle sauvegardé : models/modele.pkl")
    print("✅ Métriques : reports/metrics.json")


if __name__ == "__main__":
    main()

"""Entraînement, évaluation et sauvegarde — projet Prix des céréales (Burkina Faso).

Démarche professionnelle :
  1. séparation TEMPORELLE (aucun tirage aléatoire)
  2. baselines naïves obligatoires (persistance, saisonnier)
  3. comparaison à plusieurs horizons (1, 3, 6, 12 mois) : on ne prétend pas que
     le ML gagne partout — on mesure où il apporte de la valeur
  4. second problème : classification des flambées de prix (alerte précoce)
  5. contrôle anti-fuite automatique
  6. sauvegarde du registre de modèles + métriques + figures

Usage : python src/train.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import joblib
import lightgbm as lgb
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import (average_precision_score, confusion_matrix,
                             mean_absolute_error, mean_squared_error,
                             precision_score, recall_score, roc_auc_score, r2_score)

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE / "src"))

from features import (VARIABLES, VARIABLES_CAT, VARIABLES_NUM,  # noqa: E402
                      construire_variables, historique_complet)

HORIZONS = [1, 3, 6, 12]
FIN_TRAIN = "2023-12-31"
FIN_VALID = "2024-12-31"       # 2024 = validation (choix du seuil d'alerte)
DEBUT_TEST = "2025-01-01"      # 2025+ = test, touché une seule fois
CIBLE_RAPPEL_ALERTE = 0.60     # on veut détecter 60 % des flambées


# --------------------------------------------------------------------------- #
# Outils
# --------------------------------------------------------------------------- #
def mape(reel, pred) -> float:
    reel, pred = np.asarray(reel, float), np.asarray(pred, float)
    return float(np.mean(np.abs((reel - pred) / reel)) * 100)


def metriques_regression(reel, pred) -> dict:
    return {
        "MAE": round(mean_absolute_error(reel, pred), 2),
        "RMSE": round(float(np.sqrt(mean_squared_error(reel, pred))), 2),
        "MAPE": round(mape(reel, pred), 2),
        "R2": round(float(r2_score(reel, pred)), 3),
    }


def entrainer_lgbm_regression(X, y, **kw) -> lgb.LGBMRegressor:
    params = dict(n_estimators=800, learning_rate=0.03, num_leaves=31,
                  min_child_samples=20, subsample=0.9, colsample_bytree=0.9,
                  random_state=42, verbose=-1)
    params.update(kw)
    return lgb.LGBMRegressor(**params).fit(X, y, categorical_feature="auto")


def controle_anti_fuite(df: pd.DataFrame) -> None:
    """Vérifie qu'aucune variable ne contient d'information du mois courant.

    Méthode : on corrompt le PRIX DU MOIS COURANT (on le multiplie par 3) et on
    recalcule les variables. Si une variable change, c'est qu'elle utilisait le
    présent — donc qu'elle serait indisponible au moment de la prévision.
    """
    series = df[["produit", "region", "marche", "mois", "prix"]]
    echantillon = series.groupby(["produit", "marche"], observed=True).tail(14).copy()

    reference = construire_variables(echantillon)
    corrompu = echantillon.copy()
    index_dernier = corrompu.index[-1]
    corrompu.loc[index_dernier, "prix"] = corrompu.loc[index_dernier, "prix"] * 3
    modifie = construire_variables(corrompu)

    ecarts = []
    for col in VARIABLES_NUM:
        a, b = reference[col].iloc[-1], modifie[col].iloc[-1]
        if pd.isna(a) and pd.isna(b):
            continue
        if not np.isclose(float(a), float(b), rtol=1e-9, atol=1e-9):
            ecarts.append(col)
    if ecarts:
        raise AssertionError(
            f"❌ FUITE DE DONNÉES détectée dans : {ecarts}\n"
            "   Ces variables utilisent le prix du mois courant. Corrige features.py."
        )
    print("✅ contrôle anti-fuite : aucune variable n'utilise le mois courant")


def figure_prix(df: pd.DataFrame, chemin: Path) -> None:
    mensuel = (df.groupby(["produit", pd.Grouper(key="mois", freq="ME")], observed=True)["prix"]
                 .median().reset_index())
    plt.figure(figsize=(11, 4.5))
    for produit, bloc in mensuel.groupby("produit", observed=True):
        plt.plot(bloc["mois"], bloc["prix"], label=produit, linewidth=1.6)
    plt.axvspan(pd.Timestamp(DEBUT_TEST), mensuel["mois"].max(),
                alpha=0.12, color="red", label="période de test (2025+)")
    plt.title("Prix médians mensuels des céréales au Burkina Faso (FCFA/kg)")
    plt.xlabel("Mois"); plt.ylabel("FCFA / kg"); plt.legend(fontsize=8)
    plt.grid(alpha=0.25); plt.tight_layout(); plt.savefig(chemin, dpi=130); plt.close()


def figure_previsions(te: pd.DataFrame, chemin: Path) -> None:
    """Prévision à 12 mois : modèle contre baseline (une série de référence)."""
    ref = te[(te["produit"] == "Millet") & (te["marche"] == "Ouagadougou")]
    if ref.empty:
        ref = te[te["produit"] == "Millet"].groupby("mois", as_index=False).agg(
            cible=("cible", "mean"), pred_modele=("pred_modele", "mean"),
            pred_persistance=("pred_persistance", "mean"))
    plt.figure(figsize=(11, 4.5))
    plt.plot(ref["mois"], ref["cible"], "o-", label="prix observé", linewidth=2)
    plt.plot(ref["mois"], ref["pred_modele"], "s--", label="prévision modèle (h=12)")
    plt.plot(ref["mois"], ref["pred_persistance"], "^:", label="baseline persistance")
    plt.title("Prévision à 12 mois — Millet (FCFA/kg)")
    plt.xlabel("Mois de prévision"); plt.ylabel("FCFA / kg")
    plt.legend(fontsize=8); plt.grid(alpha=0.25); plt.tight_layout()
    plt.savefig(chemin, dpi=130); plt.close()


# --------------------------------------------------------------------------- #
# Programme principal
# --------------------------------------------------------------------------- #
def main() -> None:
    processed = RACINE / "data" / "processed" / "prix_mensuels.csv"
    if not processed.exists():
        raise SystemExit("❌ Lance d'abord : python src/preparer_donnees.py")

    brut = pd.read_csv(processed, parse_dates=["mois"])
    panel = historique_complet(construire_variables(brut[["produit", "region", "marche", "mois", "prix"]]))
    print(f"📊 {len(panel):,} observations | {panel['marche'].nunique()} marchés "
          f"| {panel['mois'].min():%Y-%m} → {panel['mois'].max():%Y-%m}".replace(",", " "))

    controle_anti_fuite(panel)
    (RACINE / "reports" / "figures").mkdir(parents=True, exist_ok=True)
    figure_prix(panel, RACINE / "reports" / "figures" / "prix_cereales.png")

    resultats: dict = {"horizons": {}, "baselines": {}}

    # ------------------------------------------------------------------ #
    # 1. RÉGRESSION : un modèle par horizon, comparé aux baselines naïves
    # ------------------------------------------------------------------ #
    print("\n" + "=" * 78)
    print("PRÉVISION DE PRIX — comparaison aux baselines naïves (test 2025+)")
    print("=" * 78)
    registre, table = {}, []

    for h in HORIZONS:
        d = panel.copy()
        d["cible"] = d.groupby(["produit", "marche"], observed=True)["prix"].shift(-(h - 1))
        d = d.dropna(subset=["cible"])
        tr = d[d["mois"] <= FIN_TRAIN]
        te = d[d["mois"] >= DEBUT_TEST]

        # modèle : on apprend la VARIATION par rapport au dernier prix connu
        modele = entrainer_lgbm_regression(tr[VARIABLES], tr["cible"] - tr["prix_lag1"])
        pred_modele = te["prix_lag1"] + modele.predict(te[VARIABLES])

        comparatif = {
            "modele": metriques_regression(te["cible"], pred_modele),
            "persistance": metriques_regression(te["cible"], te["prix_lag1"]),
            "saisonnier_12": metriques_regression(te["cible"], te["prix_lag12"]),
        }
        base = comparatif["persistance"]["MAE"]
        for nom, m in comparatif.items():
            m["MAE_vs_persistance_pct"] = round((base - m["MAE"]) / base * 100, 1)
        gagnant = min(comparatif, key=lambda k: comparatif[k]["MAE"])

        resultats["horizons"][str(h)] = {"methodes": comparatif, "meilleure_methode": gagnant}
        registre[f"h{h}"] = {"modele": modele, "type": "regression_delta"}
        table.append({"horizon": f"{h} mois", **{k: v["MAE"] for k, v in comparatif.items()},
                      "meilleure": gagnant})
        print(f"\n  horizon {h:2d} mois → meilleure méthode : {gagnant.upper()}")
        for nom, m in comparatif.items():
            print(f"     {nom:14s} MAE={m['MAE']:7.2f}  MAPE={m['MAPE']:5.2f}%  "
                  f"({m['MAE_vs_persistance_pct']:+.1f} % vs persistance)")
        if h == 12:
            te = te.assign(pred_modele=pred_modele, pred_persistance=te["prix_lag1"],
                           cible=te["cible"])
            figure_previsions(te, RACINE / "reports" / "figures" / "prevision_12_mois.png")

    print("\n" + "-" * 78)
    print(pd.DataFrame(table).to_string(index=False))

    # ------------------------------------------------------------------ #
    # 2. ALERTE PRÉCOCE : le prix va-t-il bondir de +10 % en 3 mois ?
    # ------------------------------------------------------------------ #
    print("\n" + "=" * 78)
    print("ALERTE PRÉCOCE — flambée de prix (+10 % en 3 mois)")
    print("=" * 78)
    d = panel.copy()
    d["futur3"] = d.groupby(["produit", "marche"], observed=True)["prix"].shift(-3)
    d = d.dropna(subset=["futur3"])
    d["flambee"] = (d["futur3"] > 1.10 * d["prix_lag1"]).astype(int)

    tr, va, te = (d[d["mois"] <= FIN_TRAIN],
                  d[(d["mois"] > FIN_TRAIN) & (d["mois"] <= FIN_VALID)],
                  d[d["mois"] >= DEBUT_TEST])
    print(f"taux de flambées — train {tr['flambee'].mean():.1%} | validation {va['flambee'].mean():.1%} "
          f"| test {te['flambee'].mean():.1%}")

    clf = lgb.LGBMClassifier(n_estimators=600, learning_rate=0.04, num_leaves=15,
                             min_child_samples=40, class_weight="balanced",
                             random_state=42, verbose=-1)
    clf.fit(tr[VARIABLES], tr["flambee"], categorical_feature="auto")

    # seuil choisi sur la VALIDATION (jamais sur le test)
    proba_va = clf.predict_proba(va[VARIABLES])[:, 1]
    grille = np.arange(0.15, 0.85, 0.01)
    seuil = float(min(grille, key=lambda s: abs(
        recall_score(va["flambee"], (proba_va >= s).astype(int), zero_division=0) - CIBLE_RAPPEL_ALERTE)))

    proba = clf.predict_proba(te[VARIABLES])[:, 1]
    pred = (proba >= seuil).astype(int)
    tn, fp, fn, tp = confusion_matrix(te["flambee"], pred).ravel()
    alertes = {
        "seuil": round(seuil, 2),
        "roc_auc": round(roc_auc_score(te["flambee"], proba), 3),
        "pr_auc": round(average_precision_score(te["flambee"], proba), 3),
        "taux_base_test": round(float(te["flambee"].mean()), 3),
        "rappel": round(recall_score(te["flambee"], pred, zero_division=0), 3),
        "precision": round(precision_score(te["flambee"], pred, zero_division=0), 3),
        "taux_alerte": round(float(pred.mean()), 3),
        "vrais_positifs": int(tp), "faux_positifs": int(fp),
        "faux_negatifs": int(fn), "vrais_negatifs": int(tn),
        "note": "PR-AUC à comparer au taux de base : un score de 0,26 pour une base de 0,11 "
                "signifie 2,4x mieux que le hasard",
    }
    resultats["alerte"] = alertes
    print(f"\n  ROC-AUC={alertes['roc_auc']} | PR-AUC={alertes['pr_auc']} "
          f"(base {alertes['taux_base_test']}) | gain ≈ {alertes['pr_auc']/alertes['taux_base_test']:.1f}x le hasard")
    print(f"  seuil {alertes['seuil']} → rappel={alertes['rappel']} précision={alertes['precision']} "
          f"| {alertes['taux_alerte']:.0%} des mois signalés")
    registre["alerte"] = {"modele": clf, "type": "classification", "seuil": round(seuil, 2)}

    # ------------------------------------------------------------------ #
    # 3. Sauvegarde
    # ------------------------------------------------------------------ #
    (RACINE / "models").mkdir(exist_ok=True)
    joblib.dump({"registre": registre, "variables": VARIABLES,
                 "variables_cat": VARIABLES_CAT, "horizons": HORIZONS},
                RACINE / "models" / "registre_modeles.pkl")

    resultats["meta"] = {
        "source": "WFP Food Prices for Burkina Faso (HDX), CC-BY-IGO",
        "periode_entrainement": f"→ {FIN_TRAIN}",
        "periode_test": f"{DEBUT_TEST} →",
        "n_observations": int(len(panel)),
        "n_marches": int(panel["marche"].nunique()),
        "cible_rappel_alerte": CIBLE_RAPPEL_ALERTE,
    }
    (RACINE / "reports").mkdir(exist_ok=True)
    (RACINE / "reports" / "metrics.json").write_text(
        json.dumps(resultats, indent=2, ensure_ascii=False), encoding="utf-8")

    print("\n✅ models/registre_modeles.pkl")
    print("✅ reports/metrics.json")
    print("✅ reports/figures/prix_cereales.png + prevision_12_mois.png")


if __name__ == "__main__":
    main()

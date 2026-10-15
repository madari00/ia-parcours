# 🌾 Prévision des prix céréaliers au Burkina Faso — projet de portfolio IA

[![Données](https://img.shields.io/badge/données-WFP%2FHDX%20CC--BY--IGO-blue)](https://data.humdata.org/dataset/wfp-food-prices-for-burkina-faso)
[![Python](https://img.shields.io/badge/python-3.11+-green)](https://www.python.org)
[![Tests](https://img.shields.io/badge/tests-pytest-9cf)](tests/test_api.py)

Prévision à 1, 3, 6 et 12 mois des prix du **mil, maïs et sorgho** sur **64 marchés burkinabè**, plus un **système d'alerte précoce** des flambées de prix — entraîné sur des **données réelles du Programme Alimentaire Mondial (2016-2026)**.

> **Ce projet se distingue par son honnêteté méthodologique.** J'ai construit les baselines naïves, et elles gagnent à court terme. Je le documente au lieu de le cacher : c'est ce que demande le métier en production.

---

## 1. Le problème

Au Burkina Faso, les prix des céréales de base varient brutalement (saisonnalité, insécurité, coûts de transport, spéculation). Cette volatilité frappe d'abord les ménages qui achètent au jour le jour, et les institutions (PAM, ONG, gouvernements) qui doivent anticiper leurs achats d'aide alimentaire.

**Deux besoins distincts :**
1. **Prévoir** le prix d'un marché à horizon 1-12 mois → planification des achats, stockage, budget.
2. **Alerter** quand une flambée de prix se prépare (+10 % en 3 mois) → surveillance ciblée des marchés vulnérables.

**Coût des erreurs :** une prévision trop basse fait acheter trop tard (surcoût de crise) ; une fausse alerte mobilise des ressources rares. D'où deux métriques différentes selon l'objectif : MAE/MAPE pour la prévision, rappel/precision pour l'alerte.

---

## 2. Les données (réelles)

| Élément | Détail |
|---|---|
| Source | **World Food Programme — Food Prices for Burkina Faso**, via HDX |
| Licence | Creative Commons Attribution for Intergovernmental Organisations (CC-BY-IGO) |
| Volume brut | 58 929 relevés de prix (1992-2026), 66 marchés, 13 régions |
| Retenu après nettoyage | **22 656 observations mensuelles** · 3 céréales · 64 marchés · mil/maïs/sorgho |
| Période analysée | 2016-01 → 2026-08 (prix en FCFA/kg, ventes au détail, prix réels) |
| Nettoyage | médiane mensuelle par marché (robuste aux aberrations), grille mensuelle régularisée, interpolation limitée à 2 mois de trou, filtrage des prix hors [30 ; 3 000] FCFA/kg |

---

## 3. Méthode

### Découpage temporel strict (jamais aléatoire)
| Bloc | Période | Usage |
|---|---|---|
| Entraînement | 2016-01 → 2023-12 | apprentissage |
| Validation | 2024 | **choix du seul seuil d'alerte** |
| Test | 2025-01 → 2026-08 | touché **une seule fois**, pour le rapport final |

### Anti-fuite de données
Toutes les variables sont calculables **avec les données ≤ t-1** : décalages (1, 2, 3, 6, 12 mois), moyennes mobiles décalées, variations passées, volatilité, prix national décalé, mois calendaire.
Un **test automatique** (`controle_anti_fuite`) corrompt le prix du mois courant et vérifie qu'aucune variable ne change — il s'exécute à chaque entraînement.

> 🔍 *Cette rigueur a payé : une première version affichait un MAPE de 0,2 % — signature d'une fuite. La variable « variation du mois courant » était incluse par erreur. Détectée, corrigée, et le test automatisé empêche la récidive.*

### Baselines obligatoires
- **Persistance** : prix du dernier mois connu.
- **Saisonnier** : même mois de l'année précédente.

### Modèles
- **LightGBM** par horizon, en prédisant la **variation** (`prix_{t+h} − prix_{t-1}`) plutôt que le niveau, avec variables catégorielles (produit, région, marché).
- **Classification** LightGBM (`class_weight="balanced"`) pour l'alerte de flambée.

---

## 4. Résultats mesurés (test 2025-2026, MAE en FCFA/kg)

| Horizon | Persistance | Saisonnier (-12) | Modèle ML | Meilleure méthode | Gain du ML vs persistance |
|---|---|---|---|---|---|
| 1 mois | **15,3** | 72,0 | 18,4 | persistance | −20,6 % |
| 3 mois | **30,0** | 78,4 | 35,3 | persistance | −17,8 % |
| 6 mois | **49,4** | 79,2 | 50,0 | persistance | −1,2 % |
| 12 mois | 85,3 | **74,1** | 76,6 | saisonnier (-12) | **+10,2 %** |

**Lecture honnête de ces chiffres :**
- À **1, 3 et 6 mois**, la marche aléatoire domine : les prix céréaliers sont proches d'un processus non prévisible à court terme. **Toute publication annonçant 95 % de précision sur ce type de données doit être suspectée de fuite.**
- À **6 mois**, le modèle ML rejoint la persistance (−1,2 %, dans le bruit).
- À **12 mois**, le modèle et la baseline saisonnière **battent nettement la persistance (+10 % et +13 %)** : c'est là que la saisonnalité et le retour à la moyenne apportent de l'information.
- **Conséquence opérationnelle implémentée dans l'API** : elle recommande automatiquement la méthode la plus précise à chaque horizon, au lieu de servir le modèle ML partout.

### Alerte précoce de flambée (+10 % en 3 mois)
| Métrique | Valeur | Repère |
|---|---|---|
| ROC-AUC | **0,692** | > 0,5 = apporte de l'information |
| **PR-AUC** | **0,266** | taux de base **0,114** → **2,3× mieux que le hasard** |
| Rappel au seuil 0,26 | **60,2 %** | choix métier : ne pas rater les flambées |
| Précision au seuil 0,26 | 18,9 % | coût accepté : 36 % des mois signalés |

**Usage prévu :** prioriser la surveillance de marchés, pas décider seul d'une intervention. Un rappel de 60 % pour un problème à 11 % de fréquence est un outil de tri utile ; ce n'est pas un oracle, et le README le dit.

---

## 5. Structure du dépôt

```
projet_prix_cereales/
├── README.md
├── requirements.txt · Dockerfile · .gitignore
├── src/
│   ├── preparer_donnees.py    # WFP brut → panneau mensuel propre
│   ├── features.py            # variables (partagées entraînement ↔ service)
│   └── train.py               # baselines, modèles, éval, figures, sauvegarde
├── app/
│   ├── main.py                # API FastAPI (/prevision, /alerte, /performance)
│   └── ui.py                  # interface Streamlit (3 onglets)
├── tests/test_api.py          # 9 tests (dont reproductibilité et exposé des baselines)
├── data/raw/                  # données WFP brutes
├── data/processed/            # panneau mensuel
├── models/registre_modeles.pkl
└── reports/                   # metrics.json + figures
```

---

## 6. Lancer le projet

```bash
pip install -r requirements.txt

# 1. Données (le CSV brut est déjà dans data/raw/)
python src/preparer_donnees.py
#    Si besoin, retélécharger : https://data.humdata.org/dataset/wfp-food-prices-for-burkina-faso

# 2. Entraînement + évaluation (≈ 30 s)
python src/train.py
#    → affiche le contrôle anti-fuite, les 4 horizons comparés aux baselines, l'alerte

# 3. API
uvicorn app.main:app --host 0.0.0.0 --port 8000
#    → http://localhost:8000/docs

# 4. Interface
streamlit run app/ui.py

# 5. Tests
pytest -q
```

**Exemple d'appel :**
```bash
curl -X POST http://localhost:8000/alerte -H "Content-Type: application/json" -d '{
  "produit": "Millet", "marche": "Ouahigouya", "region": "NORD", "prix_national_lag1": 265.0,
  "historique": [{"mois":"2025-01","prix":243},{"mois":"2025-02","prix":246},
                 {"mois":"2025-03","prix":249},{"mois":"2025-04","prix":252},
                 {"mois":"2025-05","prix":255},{"mois":"2025-06","prix":258},
                 {"mois":"2025-07","prix":261},{"mois":"2025-08","prix":264},
                 {"mois":"2025-09","prix":267},{"mois":"2025-10","prix":270},
                 {"mois":"2025-11","prix":273},{"mois":"2025-12","prix":276},
                 {"mois":"2026-01","prix":279}]}'
```

---

## 7. Ce que je ferais ensuite (limites assumées)

1. **Ajouter des variables exogènes** : pluviométrie (CHIRPS), NDVI, prix du carburant, événements de sécurité (ACLED), taux de change. C'est là que se trouve le signal manquant à court terme.
2. **Passer à l'échelle régionale** : comparer le Burkina aux pays voisins (transmission des prix transfrontalière, modèles spatiaux).
3. **Modéliser l'incertitude** : intervalles de prédiction (régression quantile) plutôt qu'une valeur unique — indispensable pour une décision publique.
4. **Suivre la dérive** (drift) : le régime de prix change (crises 2020-2022) ; prévoir une surveillance mensuelle des distributions et un réentraînement glissant.
5. **Biais connu** : `prix_national_lag1` est optionnel ; s'il n'est pas fourni, le ratio vaut 1 pour un marché isolé, ce qui éloigne légèrement de la distribution d'entraînement. À corriger en production en alimentant systématiquement la valeur nationale.

---

## 8. Compétences démontrées

`Python` · `pandas` · `LightGBM` · `scikit-learn` · **analyse de séries temporelles** · **validation temporelle** · **détection de fuite de données** · **conception de baselines** · **choix de métrique selon le coût des erreurs** · `matplotlib` · `FastAPI` + `pydantic` · `Streamlit` · `pytest` · `Docker` · **communication de résultats (README, limites, honnêteté)**

---

*Données : World Food Programme, via le Humanitarian Data Exchange. Un modèle qui ne publie pas ses baselines n'est pas un modèle, c'est une publicité.*

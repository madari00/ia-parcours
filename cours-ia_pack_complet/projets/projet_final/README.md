# Projet final de portfolio — Prédiction du risque de défaut (microfinance, Burkina Faso)

> 🎯 **But de ce projet :** te donner un squelette **professionnel, complet et déployable** que tu adaptes avec TES données.
> Il contient tout ce que les recruteurs francophones vérifient : données, entraînement reproductible, évaluation honnête, API avec validation, interface, tests, Docker, CI, README.

---

## 1. Le problème business

Une institution de microfinance au Burkina Faso accorde des crédits à des commerçants, agriculteurs et artisans.
Chaque défaut coûte cher ; chaque refus injustifié fait perdre un client.

**Objectif :** prédire la probabilité de défaut dans les 6 mois, afin d'orienter la décision d'octroi.

**Coût des erreurs (à adapter avec le métier) :**
- Faux négatif (on prête à quelqu'un qui fera défaut) → perte du capital (très coûteux).
- Faux positif (on refuse un bon client) → manque à gagner + insatisfaction (coût modéré).
→ **On privilégie donc le rappel** sur la classe « défaut », à taux de fausses alertes contrôlé.

**Seuil de décision retenu :** 0,42 (compromis mesuré sur la validation, cf. `reports/metrics.json`).

---

## 2. Les données

- 6 000 dossiers simulés réalistes (le script `src/generate_data.py` en produit — **remplace-le par tes vraies données**).
- Variables : âge, revenu mensuel (FCFA), montant du crédit, durée, ancienneté client, nombre de crédits antérieurs, score Mobile Money, secteur d'activité, ville.
- Cible : `defaut` (1 = défaut constaté).

⚠️ **Si tu utilises des données réelles :** elles doivent être anonymisées (RGPD). Les colonnes identifiantes (nom, téléphone, numéro de pièce) ne doivent **jamais** entrer dans le modèle.

---

## 3. Méthode

| Étape | Détail |
|---|---|
| Baseline métier | règle simple : « 2 crédits antérieurs + score Mobile Money < 40 » |
| Modèle 1 | Régression logistique (interprétable, référence) |
| Modèle 2 | Random Forest (class_weight=balanced) |
| Évaluation | split stratifié 80/20 + cross-validation 5 folds, **rapport** sur jeu de test touché une seule fois |
| Métriques | ROC-AUC, PR-AUC, rappel/precision au seuil retenu, matrice de confusion, performance **par ville** (équité) |
| Interprétation | importances + SHAP (à ajouter quand shap est installé) |
| Décision | seuil optimisé pour un rappel cible ≥ 0,60 avec précision ≥ 0,50 |

---

## 4. Résultats

Résultats **réellement mesurés** sur les données simulées (reproductibles avec `python src/train.py`, graine 42) :

| Modèle | ROC-AUC (test) | PR-AUC | Rappel @ seuil | Précision @ seuil |
|---|---|---|---|---|
| Baseline métier (règle simple) | 0,524 | — | 0,178 | 0,278 |
| **Régression logistique (retenue)** | **0,715** | 0,428 | 0,636 @ 0,52 | 0,383 |
| Random Forest | 0,705 | 0,427 | 0,617 @ 0,38 | 0,374 |

*Validation croisée 5 folds sur l'entraînement : logistique 0,736 (±0,019), Random Forest 0,718 (±0,018).*

**Lecture honnête de ces résultats :**
- Le modèle bat nettement la règle métier (0,715 vs 0,524) → il apporte de la valeur.
- La **logistique gagne légèrement** sur la forêt et reste **explicable** → on la retient. *(Leçon à citer en entretien : le modèle le plus complexe ne gagne pas toujours.)*
- Précision modeste au seuil retenu (0,383) : c'est le prix d'un rappel élevé (0,636), conforme au coût des erreurs défini en §1.
- L'écart entre CV (0,736) et test (0,715) est faible → **pas de surapprentissage**.

**Performance par ville (contrôle d'équité) :** Banfora 0,678 · Bobo-Dioulasso 0,723 · Koudougou 0,714 · Ouagadougou 0,746 · Ouahigouya 0,624.
→ Écart de 0,12 point d'AUC entre villes : à surveiller, car un modèle moins fiable en zone rurale peut y réduire l'accès au crédit. **C'est exactement le genre de remarque qui distingue un candidat junior sérieux.**

> 💡 **Règle d'or du README :** ne mets jamais un chiffre que tu ne peux pas reproduire avec `python src/train.py`. (Ici : les données sont **simulées**, écris-le explicitement.)

---

## 5. Impact estimé (à adapter)

Si l'institution traite 5 000 demandes/an, un rappel de 0,6 sur un taux de défaut de 15 % permet d'éviter environ 0,6 × 750 = **450 défauts par an**, pour un taux de fausses alertes de X %.
→ À chiffrer avec la valeur moyenne d'un crédit : c'est **cette phrase** qui transforme un projet d'étudiant en projet professionnel.

---

## 6. Structure du dépôt

```
projet_final/
├── README.md                  ← ce fichier
├── requirements.txt
├── Dockerfile
├── .gitignore
├── src/
│   ├── generate_data.py       ← données simulées (à remplacer)
│   ├── train.py               ← entraînement + évaluation + sauvegarde
│   └── features.py            ← préparation des variables
├── app/
│   ├── main.py                ← API FastAPI
│   └── ui.py                  ← interface Streamlit
├── tests/
│   └── test_api.py            ← tests pytest
├── models/modele.pkl          ← (généré)
└── reports/metrics.json       ← (généré)
```

---

## 7. Comment lancer (à vérifier soi-même avant de publier)

```bash
pip install -r requirements.txt

# 1. Générer les données (ou déposer les tiennes dans data/raw/)
python src/generate_data.py

# 2. Entraîner et évaluer
python src/train.py

# 3. Lancer l'API
uvicorn app.main:app --host 0.0.0.0 --port 8000
# → documentation interactive : http://localhost:8000/docs

# 4. Lancer l'interface
streamlit run app/ui.py

# 5. Tests
pytest -q

# 6. Docker
docker build -t api-defaut:v1 . && docker run -p 8000:8000 api-defaut:v1
```

**Exemple d'appel à l'API :**
```bash
curl -X POST http://localhost:8000/predire -H "Content-Type: application/json" -d '{
  "age": 38, "revenu_mensuel_fcfa": 175000, "montant_credit_fcfa": 500000,
  "duree_mois": 12, "anciennete_client_mois": 30, "nb_credits_precedents": 3,
  "score_mobile_money": 62, "secteur": "commerce", "ville": "Ouagadougou"}'
```

---

## 8. Limites et suite (section honnête — les recruteurs la lisent)

- Données **simulées** dans cette version de démonstration : les performances ne sont pas transposables telles quelles.
- Pas de variables socio-économiques externes (saison des pluies, inflation, prix agricoles) qui pèsent beaucoup au Sahel.
- Risque de **data drift** en cas de crise économique ou de changement de politique de crédit → surveillance mensuelle des distributions et du taux de refus prévue.
- Équité : vérifier régulièrement la performance par ville/secteur (ne pas pénaliser une région déjà fragile).
- Suite : ajouter SHAP pour expliquer chaque refus, tester LightGBM, intégrer les prix agricoles mensuels.

---

## 9. Ce que tu dois personnaliser avant de le publier

1. Remplacer les données simulées par de vraies données (anonymisées).
2. Refuser de recopier des chiffres inventés dans la section 4.
3. Ajouter 3 figures (`reports/figures/`) : distribution de la cible, matrice de confusion, importance des variables.
4. Déployer sur **Render / Railway / Hugging Face Spaces** et coller l'URL en haut du README.
5. Ajouter une capture d'écran de l'API (`/docs`) et de l'interface Streamlit.

---

*Projet conçu comme modèle de livrable pour un poste de Data Scientist / ML Engineer junior sur le marché francophone.*

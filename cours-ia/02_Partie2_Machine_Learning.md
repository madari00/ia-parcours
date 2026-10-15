# PARTIE 2 — MACHINE LEARNING : le cœur du métier

> **Durée prévue :** semaines 13 à 26 (5-10 h/semaine)
> **Objectif de fin de partie :** tu sais mener un projet ML **de bout en bout** : données brutes → nettoyage → modèle → évaluation honnête → interprétation → restitution.
> **C'est la partie qui te rend employable.** Le deep learning épate, mais 70 % des offres « data/IA » en France, Belgique, Suisse et Québec demandent d'abord ça.

---

| Chapitre | Sujet | Semaines |
|---|---|---|
| 7 | Panorama du ML : les 4 familles | 13 |
| 8 | Le workflow ML complet | 13-15 |
| 9 | Évaluation honnête d'un modèle | 15-17 |
| 10 | Les modèles simples (à comprendre à fond) | 17-19 |
| 11 | Arbres, forêts et boosting (les champions) | 19-21 |
| 12 | Non supervisé : clusters et réduction de dimension | 21-23 |
| 13 | Projet ML complet + interprétabilité | 23-26 |

---

# CHAPITRE 7 — Panorama : les 4 familles du machine learning

### 🎯 Objectif
Savoir nommer et reconnaître le type de problème avant de coder. **50 % des erreurs de débutants viennent d'avoir mal posé le problème.**

### 💡 L'essentiel en 5 minutes

| Famille | Tu as des étiquettes ? | Question type | Exemple |
|---|---|---|---|
| **Supervisé — régression** | oui, un **nombre** | « Combien ? » | prix du sorgho demain, durée de trajet |
| **Supervisé — classification** | oui, une **catégorie** | « Quelle classe ? » | spam/pas spam, maladie A/B/C |
| **Non supervisé** | non | « Quels groupes ? » | segmenter des clientes, détecter des anomalies |
| **Renforcement** | non, mais des **récompenses** | « Quelle action ? » | robot, jeu, enchères publicitaires |

**95 % des emplois junior** en France/Belgique/Suisse/Québec : **supervisé** (régression + classification) + un peu de non supervisé. Le renforcement est un bonus rare (jeux, robotique, énergie, trading).

### 📘 Le cours

#### 7.1 Le vocabulaire exact (à connaître en FR et EN pour les entretiens)
| Français | Anglais | Définition |
|---|---|---|
| Caractéristique | feature / variable | une colonne d'entrée |
| Cible | target / label | ce qu'on prédit |
| Étiquette | label | valeur de la cible |
| Jeu d'entraînement | training set | données pour apprendre |
| Jeu de validation | validation set | données pour régler |
| Jeu de test | test set | données pour l'évaluation finale |
| Surapprentissage | overfitting | le modèle apprend le bruit par cœur |
| Sous-apprentissage | underfitting | le modèle est trop simple |
| Régularisation | regularization | pénaliser la complexité |
| Fonction de coût | loss / cost function | l'erreur à minimiser |

#### 7.2 Supervisé vs non supervisé : la différence en une image
- **Supervisé** = apprendre avec un **professeur** qui te donne les réponses. Tu corriges jusqu'à tomber juste.
- **Non supervisé** = ranger une chambre **sans consigne** : tu regroupes par ressemblance. Personne ne te dit si tu as bon.

#### 7.3 Classification binaire vs multiclasse vs multi-étiquettes
- **Binaire** : 2 classes. Le modèle sort **une probabilité** (ex. 0,87 de risque). On choisit un **seuil** (souvent 0,5, mais pas toujours !).
- **Multiclasse** : N classes mutuellement exclusives (A, B, C). Sortie = distribution de probabilités qui somme à 1 (softmax).
- **Multi-étiquettes** : plusieurs classes *en même temps* (une photo peut contenir « arbre » ET « personne »).

#### 7.4 Les questions à se poser AVANT de coder (checklist de cadrage)
1. **Quel est l'objectif business ?** (« réduire de 20 % les ruptures de stock », pas « faire un modèle »)
2. **Quelle décision sera prise grâce à la prédiction ?** (sinon, à quoi bon ?)
3. **Quelle est la ligne de base (baseline) ?** Quel score fait la méthode toute bête (ex. « prédire la moyenne », « prédire la classe majoritaire ») ? Si ton modèle ne la bat pas, il ne sert à rien.
4. **Quel coût ont les erreurs ?** Un faux négatif (rater un malade) et un faux positif (inquiéter à tort) n'ont pas le même prix → cela détermine les métriques.
5. **Quelles données ai-je le droit d'utiliser ?** (RGPD en Europe, consentement, données personnelles, données sensibles).
6. **Comment ce modèle vivra dans le monde réel ?** (batch la nuit ? API temps réel ? qui le surveille ?)

### ⚠️ Les 3 erreurs classiques
1. **Commencer par le modèle** au lieu de l'objectif. Un modèle parfait sur la mauvaise question = zéro.
2. **Sauter la baseline.** 40 % des « modèles IA » présentés en entreprise font moins bien qu'une simple règle métier.
3. **Ignorer le coût des erreurs.** On ne choisit les métriques qu'après avoir chiffré ce coût.

### ✅ Quiz
1. Pour prédire « le client va-t-il résilier ? » : quelle famille, quel type ?
2. Pour regrouper des magasins par profil de ventes : quelle famille ?
3. Qu'est-ce qu'une baseline et pourquoi est-ce indispensable ?
4. Traduis en anglais : surapprentissage, jeu de validation, fonction de coût.
5. Pourquoi le seuil de décision n'est-il pas toujours 0,5 ?

### 🛠️ Exercice (écrit, 30 min)
Écris un fichier `cadrage_projet.md` pour TON projet fil rouge, avec les 6 points de la checklist 7.4 et un tableau « coût des erreurs ».

---

# CHAPITRE 8 — Le workflow ML complet

### 🎯 Objectif
Maîtriser la séquence standard que tu répéteras toute ta carrière, et éviter le **data leakage** (la faute professionnelle n°1).

### 💡 L'essentiel en 5 minutes

```
1. Comprendre le besoin       →  6. Entraîner
2. Collecter les données      →  7. Évaluer sur validation
3. Explorer (EDA)             →  8. Ajuster les hyperparamètres
4. Nettoyer / préparer        →  9. Évaluer UNE FOIS sur le test
5. Séparer train/val/test     → 10. Déployer et surveiller
```

La règle qui sauve ta carrière : **le jeu de test ne sert qu'une seule fois, à la toute fin.** Si tu le regardes pour choisir ton modèle, tu ne mesures plus rien : tu triches (sans le vouloir).

### 📘 Le cours

#### 8.1 Explorer les données (EDA)
```python
df.head(); df.info(); df.describe(); df.isna().sum()
df["cible"].value_counts(normalize=True)   # équilibre des classes
df.corr(numeric_only=True)["cible"].sort_values()   # corrélations avec la cible
```
Puis **3 graphiques minimum** : distribution de la cible, cible vs 2 variables clés, matrice de corrélation.
**Écris tes observations en français dans le notebook.** Les recruteurs cherchent des gens qui *comprennent* les données, pas des exécutants de `.fit()`.

#### 8.2 Les fuites de données (data leakage) : 4 formes courantes
1. **Normaliser/imputer avant la séparation** → les stats du test contaminent le train.
2. **Utiliser une variable qui contient la réponse** (ex. : prédire « a résilié » avec la colonne « date de résiliation »). Le modèle aura 99 %… et sera inutile.
3. **Mélanger temporel** : prédire le passé avec des données du futur. En série temporelle, **on coupe par date**, jamais au hasard.
4. **Ré-échantillonner avant la séparation** (SMOTE sur tout le dataset). ⚠️ Un chercheur s'est fait retirer un article pour ça — c'est LE classique.

#### 8.3 Séparer les données
```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y  # stratify = garder les proportions de classes
)
# Puis, dans le train : X_train, X_val = train_test_split(X_train, test_size=0.2, ...)
```
En **série temporelle**, pas de hasard :
```python
# 80 % du début pour le train, 20 % de la fin pour le test
cut = int(len(df) * 0.8)
train, test = df.iloc[:cut], df.iloc[cut:]
```

#### 8.4 Préparer les variables
| Problème | Solution | Code |
|---|---|---|
| Valeurs manquantes (numérique) | imputer par la médiane | `SimpleImputer(strategy="median")` |
| Valeurs manquantes (catégoriel) | imputer par la valeur la plus fréquente | `SimpleImputer(strategy="most_frequent")` |
| Texte → nombres | one-hot encoding | `OneHotEncoder(handle_unknown="ignore")` |
| Ordre naturel (petit<moyen<grand) | encodage ordinal | `OrdinalEncoder(categories=[...])` |
| Échelles différentes | standardisation | `StandardScaler()` |
| Très grande échelle / skew | transformation log | `np.log1p(x)` |
| Colonnes très asymétriques | quantiles | `QuantileTransformer` |

**Le Pipeline : le bon réflexe professionnel** — il empêche les fuites, parce que toutes les transformations sont **apprises sur le train uniquement** :
```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

num = ["age", "revenu"]
cat = ["ville", "profession"]

prep = ColumnTransformer([
    ("num", Pipeline([("imp", SimpleImputer(strategy="median")),
                      ("sc", StandardScaler())]), num),
    ("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")),
                      ("oh", OneHotEncoder(handle_unknown="ignore"))]), cat),
])
```

#### 8.5 Les classes déséquilibrées (fréquent en fraude, maladie, panne)
Stratégies, dans l'ordre :
1. **Métriques adaptées** (rappel, F1, PR-AUC) — souvent suffisant et gratuit.
2. **`class_weight="balanced"`** — le plus simple à essayer.
3. **Seuil de décision ajusté** (le plus efficace en pratique).
4. **Ré-échantillonnage** : `imblearn` (SMOTE *dans* le pipeline, sur le train seulement).
5. **Modèles adaptés** (boosting avec `scale_pos_weight`).

#### 8.6 Le réglage des hyperparamètres
- **Grid Search** : on teste toutes les combinaisons (lent mais systématique).
- **Random Search** : tirages aléatoires (souvent meilleur rapport temps/résultat).
- **Optuna** (bayésien) : standard moderne.
```python
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint
search = RandomizedSearchCV(model, {"n_estimators": randint(50, 400),
                                    "max_depth": randint(2, 20)},
                            n_iter=30, cv=5, scoring="roc_auc", random_state=42)
search.fit(X_train, y_train)
print(search.best_params_, search.best_score_)
```

### ⚠️ Les 3 erreurs classiques
1. **Leakage via le pré-traitement** (chapitre 8.2). Utilise des Pipelines.
2. **Trop de préparation manuelle dans le notebook** : à la fin, tout doit être dans un pipeline réutilisable, sinon ton modèle ne sera jamais déployable.
3. **Optimiser indéfiniment sur la validation.** Au bout de 50 essais, tu commences à sur-apprendre la validation ; garde le test intact pour un jugement final honnête.

### 💻 Code du chapitre (squelette de projet à garder)
```python
import numpy as np, pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score

# 1. Données jouet
rng = np.random.default_rng(0)
n = 400
df = pd.DataFrame({
    "age": rng.integers(18, 70, n),
    "revenu": rng.lognormal(11, 0.6, n).round(0),
    "ville": rng.choice(["Ouaga", "Bobo", "Koudougou"], n),
})
# cible : risque de défaut (dépend de l'âge et du revenu, avec du bruit)
score = -0.03 * df["age"] - 0.000004 * df["revenu"] + rng.normal(0, 0.7, n)
df["defaut"] = (score > np.quantile(score, 0.75)).astype(int)

# 2. Split stratifié
X, y = df.drop(columns="defaut"), df["defaut"]
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 3. Pipeline complet
prep = ColumnTransformer([
    ("num", Pipeline([("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler())]), ["age", "revenu"]),
    ("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")), ("oh", OneHotEncoder(handle_unknown="ignore"))]), ["ville"]),
])
modele = Pipeline([("prep", prep), ("clf", RandomForestClassifier(n_estimators=300, random_state=42, class_weight="balanced"))])

# 4. Entraînement + évaluation
modele.fit(X_tr, y_tr)
proba = modele.predict_proba(X_te)[:, 1]
print("ROC-AUC :", round(roc_auc_score(y_te, proba), 3))
print(classification_report(y_te, (proba > 0.5).astype(int)))
```

### ✅ Quiz
1. Cite 3 formes de data leakage.
2. Pourquoi mettre les transformations dans un `Pipeline` plutôt que les appliquer à la main ?
3. Comment séparer des données de série temporelle ?
4. Dans quel ordre échantillonner/imputer/standardiser/séparer ?
5. Quand utiliser Random Search plutôt que Grid Search ?

### 🛠️ Exercice
Reprends un dataset réel (Kaggle « Titanic », « Credit Card Fraud » ou données locales) et écris un `workflow.ipynb` respectant exactement les étapes 1→9. **Zéro fuite** : tu vérifieras avec la checklist 8.2.

---

# CHAPITRE 9 — Évaluation honnête : la compétence qui te distinguera

### 🎯 Objectif
Choisir LA bonne métrique, lire une matrice de confusion, détecter l'overfitting et l'expliquer en entretien.

### 💡 L'essentiel en 5 minutes

Un modèle n'est pas « bon » dans l'absolu : il est bon **pour un objectif**. Voici comment on en parle sans se tromper :

- **Accuracy** (exactitude) = % de bonnes réponses. **Trompeuse si les classes sont déséquilibrées.**
- **Précision** = parmi mes alertes, combien sont justes ? (« quand je dis oui, ai-je raison ? »)
- **Rappel (recall / sensibilité)** = parmi les vrais cas, combien j'en attrape ? (« en ai-je raté ? »)
- **F1** = compromis précision/rappel (moyenne harmonique).
- **AUC-ROC** = pouvoir de classement, indépendant du seuil.

### 📘 Le cours

#### 9.1 La matrice de confusion (à dessiner de mémoire en entretien)
|  | Prédit Négatif | Prédit Positif |
|---|---|---|
| **Réel Négatif** | Vrai Négatif (VN) | Faux Positif (FP) ← « fausse alerte » |
| **Réel Positif** | Faux Négatif (FN) ← « raté » | Vrai Positif (VP) |

$$\text{Précision} = \frac{VP}{VP+FP} \qquad \text{Rappel} = \frac{VP}{VP+FN} \qquad F_1 = \frac{2\,\text{Précision}\cdot\text{Rappel}}{\text{Précision}+\text{Rappel}}$$

**La tension fondamentale :** augmenter le rappel fait souvent baisser la précision (et inversement). C'est un **arbitrage**, pas un défaut. À toi de choisir selon le coût des erreurs.

**Exemples concrets :**
- **Dépistage du cancer** → on privilégie le **rappel** (mieux vaut une fausse alerte qu'un cancer raté).
- **Filtre anti-spam** → on privilégie la **précision** (mieux vaut laisser passer un spam que bloquer un mail professionnel).
- **Détection de fraude bancaire** → compromis piloté par le coût réel de chaque erreur (souvent F1 ou PR-AUC).

#### 9.2 Courbe ROC et AUC
La courbe ROC trace **Taux de Vrais Positifs** contre **Taux de Faux Positifs** pour tous les seuils possibles.
- **AUC = 0,5** → le modèle ne fait pas mieux que le hasard.
- **AUC = 0,7-0,8** → correct. **0,8-0,9** → bon. **> 0,9** → excellent (méfie-toi : vérifie les fuites !)
Si les classes sont très déséquilibrées (<5 % de positifs), préfère la courbe **Précision-Rappel** et son **PR-AUC**.

#### 9.3 Métriques de régression
| Métrique | Formule | Sensibilité aux extrêmes | Interprétation |
|---|---|---|---|
| **MAE** | $\frac{1}{n}\sum\|y-\hat y\|$ | faible | erreur moyenne en unité réelle (recommandée) |
| **RMSE** | $\sqrt{\frac{1}{n}\sum(y-\hat y)^2}$ | **forte** | pénalise les grosses erreurs |
| **R²** | $1 - \frac{\sum(y-\hat y)^2}{\sum(y-\bar y)^2}$ | — | 1 = parfait, 0 = aussi bien que la moyenne, <0 = pire |

⚠️ **Toujours comparer à une baseline** : un R² de 0,3 peut être excellent si la baseline fait 0,05, et catastrophique si la baseline fait 0,6.

#### 9.4 Overfitting / underfitting : les 4 diagnostics
| Symptôme | Diagnostic | Remède |
|---|---|---|
| Train très bon, test mauvais | **overfitting** | plus de données, régularisation, modèle plus simple, early stopping, dropout |
| Train mauvais, test mauvais | **underfitting** | modèle plus complexe, meilleures features, entraîner plus longtemps |
| Train bon, validation instable (grand écart selon les folds) | **variance élevée** | plus de données, cross-validation plus robuste, ensembles |
| Loss de validation remonte pendant l'entraînement | **overfitting en cours** | **early stopping** (arrêter au minimum) |

**Règle pratique :** l'écart train/validation doit rester **petit**. Si l'écart est gros, tu mens à ton employeur (sans le vouloir) en annonçant ton score du train.

#### 9.5 Validation croisée (cross-validation)
```python
from sklearn.model_selection import cross_val_score
scores = cross_val_score(modele, X, y, cv=5, scoring="roc_auc")
print(scores, scores.mean(), scores.std())
```
- **K-fold (k=5)** : on découpe en 5, on entraîne 5 fois en laissant un bloc de côté. Donne une estimation **plus fiable** qu'un seul split.
- **Stratified K-fold** : conserve les proportions de classes → par défaut en classification.
- **TimeSeriesSplit** : pour les séries temporelles (jamais de hasard !).
- **GroupKFold** : quand des lignes sont liées (ex. plusieurs mesures du même patient — sinon fuite entre folds).

### ⚠️ Les 3 erreurs classiques
1. **Annoncer l'exactitude** (accuracy) sur un problème déséquilibré.
2. **Choisir le modèle avec le meilleur score sur le test** → c'est de la triche ; le test est un juge, pas un entraîneur.
3. **Ne regarder qu'un chiffre.** Regarde toujours : métrique principale + matrice de confusion + dispersion de la CV + erreurs concrètes (quels exemples sont mal prédits ?).

### 💻 Code du chapitre
```python
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import confusion_matrix, roc_auc_score, classification_report

X, y = make_classification(n_samples=2000, n_features=12, n_informative=6,
                           weights=[0.9, 0.1], random_state=0)   # 10 % de positifs
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)

m = LogisticRegression(max_iter=1000, class_weight="balanced").fit(X_tr, y_tr)
p = m.predict_proba(X_te)[:, 1]

print("Accuracy (trompeuse) :", round((m.predict(X_te) == y_te).mean(), 3))
print("ROC-AUC :", round(roc_auc_score(y_te, p), 3))
print(confusion_matrix(y_te, p > 0.5))
print(classification_report(y_te, p > 0.5, digits=3))
print("CV ROC-AUC :", cross_val_score(m, X, y, cv=5, scoring="roc_auc").round(3))
```

### ✅ Quiz
1. Un modèle anti-spam avec 99 % d'accuracy : suffisant ? Pourquoi ?
2. Différence entre précision et rappel, en une phrase chacun ?
3. Ton modèle a R²_train = 0,98 et R²_test = 0,41. Diagnostic et 3 remèdes ?
4. Quand utiliser le PR-AUC plutôt que le ROC-AUC ?
5. Pourquoi la cross-validation est-elle plus fiable qu'un seul split ?

### 🛠️ Exercices
1. Sur le dataset **Credit Card Fraud** (Kaggle), entraîne une régression logistique, puis affiche accuracy, précision, rappel, F1, PR-AUC. Compare avec un modèle qui prédit « toujours normal ». Rédige 5 lignes de conclusion.
2. Trace la courbe ROC de ton modèle et commente l'AUC.
3. Fais varier le seuil de 0,1 à 0,9 et note précision/rappel. Trouve le seuil qui maximise le F1, puis celui qui maximise le rappel ≥ 0,9. Explique lequel tu recommanderais à ta banque et pourquoi.
4. Régression : sur un dataset de prix, calcule MAE, RMSE, R², et compare à la baseline « prédire la moyenne ».

---

# CHAPITRE 10 — Les modèles simples (à comprendre avant tout le reste)

### 🎯 Objectif
Comprendre 4 modèles fondamentaux : régression linéaire, régression logistique, k-NN, arbre de décision. **On commence toujours par ceux-là** — et souvent, ils suffisent.

### 💡 L'essentiel en 5 minutes

- **Régression linéaire** : trace la droite qui passe au plus près des points.
- **Régression logistique** : même chose, puis on compresse le résultat entre 0 et 1 → une probabilité.
- **k-NN** : « dis-moi qui sont tes voisins, je te dirai qui tu es ».
- **Arbre de décision** : une suite de questions oui/non (« revenu > 30 000 ? » → « âge < 25 ? » → …).

### 📘 Le cours

#### 10.1 Régression linéaire
Modèle : $\hat{y} = w_1x_1 + w_2x_2 + \dots + b = Xw + b$.

**Comment on trouve w ?** Deux voies :
1. **Formule analytique** (moindres carrés) : $w = (X^TX)^{-1}X^Ty$ — exacte mais coûteuse et instable sur beaucoup de variables.
2. **Descente de gradient** (chapitre 5) — c'est ce qu'on utilise en pratique.

**Hypothèses à vérifier** : relation plutôt linéaire, erreurs homogènes, pas de multicolinéarité forte (deux variables très corrélées).
**Régularisation** (essentiel) :
- **Ridge (L2)** : pénalise la somme des carrés des poids → réduit les coefficients, gère la multicolinéarité.
- **Lasso (L1)** : pénalise la somme des valeurs absolues → met certains coefficients **exactement à 0** (sélection automatique de variables).
- **ElasticNet** : mélange des deux.
```python
from sklearn.linear_model import Ridge, Lasso
for alpha in [0.01, 0.1, 1, 10]:
    Ridge(alpha=alpha).fit(X_tr, y_tr)   # alpha grand = modèle plus contraint
```

#### 10.2 Régression logistique (le cheval de trait de la classification)
Étapes : 1) calcul linéaire $z = Xw+b$ ; 2) **fonction sigmoïde** pour comprimer dans ]0,1[.
$$\sigma(z) = \frac{1}{1 + e^{-z}}$$
3) Décision : si $\sigma(z) > 0{,}5$ → classe 1.
Entraînement : minimiser **l'entropie croisée** (log-loss) — équivalent à maximiser la vraisemblance des données observées.

**Pourquoi c'est essentiel :** c'est **le** modèle de référence en milieu professionnel (crédit, assurance, santé, marketing), parce qu'il est rapide, stable, **interprétable** (chaque coefficient = un effet marginal, exprimé en *odds ratio*), et souvent aussi performant que des modèles complexes quand les données sont propres.

```python
from sklearn.linear_model import LogisticRegression
lr = LogisticRegression(max_iter=2000, C=1.0, class_weight="balanced").fit(X_tr, y_tr)
print(dict(zip(features, lr.coef_[0].round(3))))   # signe = sens de l'effet
```
`C` = inverse de la force de régularisation (petit C = plus régularisé).

#### 10.3 k-NN (k plus proches voisins)
Principe : pour un nouvel exemple, on regarde ses **k voisins** les plus proches (distance euclidienne ou cosinus) et on vote.
- **Avantages** : ultra simple, aucune hypothèse, bon en démonstration.
- **Inconvénients** : lent en prédiction sur gros volumes ; **exige la normalisation** (sinon une variable en euros écrase tout) ; souffre en haute dimension (malédiction de la dimension).
- **k est un hyperparamètre** : petit k = bruité (variance), grand k = trop lisse (biais). On teste 3, 5, 11, 21…
```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
knn = Pipeline([("sc", StandardScaler()), ("knn", KNeighborsClassifier(n_neighbors=11))]).fit(X_tr, y_tr)
```

#### 10.4 Arbre de décision
Principe : à chaque nœud, on choisit la question qui **sépare le mieux** les classes.
- Mesure de pureté : **Gini** ou **entropie**. Objectif : maximiser le **gain d'information**.
$$\text{Gini} = 1 - \sum_c p_c^2 \qquad \text{Entropie} = -\sum_c p_c \log_2 p_c$$
- **Contrôles** : `max_depth`, `min_samples_leaf`, `min_samples_split`.
- **Avantages** : très **interprétable** (utilisable devant un comité de crédit, une préfecture, un client).
- **Inconvénients** : **instable** (un petit changement de données change tout l'arbre) et overfitte facilement → c'est pourquoi on passe aux forêts (chapitre 11).
```python
from sklearn.tree import DecisionTreeClassifier, plot_tree
tree = DecisionTreeClassifier(max_depth=4, min_samples_leaf=20, random_state=0).fit(X_tr, y_tr)
# plot_tree(tree)   # visualisation : la force de l'arbre
```

#### 10.5 Tableau comparatif (à savoir réciter en entretien)
| Modèle | Interprétable | Rapide | Nonlinearités | Données manquantes | Candidat par défaut |
|---|---|---|---|---|---|
| Régression linéaire | ⭐⭐⭐ | ⭐⭐⭐ | ❌ | ❌ | oui (régression) |
| Régression logistique | ⭐⭐⭐ | ⭐⭐⭐ | ❌ | ❌ | **oui (classification)** |
| k-NN | ⭐ | ⭐ | ✅ | ❌ | non |
| Arbre seul | ⭐⭐⭐ | ⭐⭐⭐ | ✅ | ⚠️ (sklearn non) | démonstration |
| Random Forest | ⭐⭐ | ⭐⭐ | ✅ | ⚠️ | oui |
| Gradient Boosting | ⭐⭐ (SHAP) | ⭐⭐ | ✅ | ⚠️ | **souvent le meilleur** |

### ⚠️ Les 3 erreurs classiques
1. **Entraîner k-NN ou logistique sans normaliser** → résultats absurdes.
2. **Utiliser un arbre profond sans limite** → overfitting garanti.
3. **Conclure « linéaire = mauvais »** sans essayer. Souvent la logistique régularisée gagne sur des données tabulaires réelles, et elle se défend en réunion.

### 💻 Code du chapitre (les 4 modèles côte à côte)
```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

X, y = make_classification(n_samples=1500, n_features=15, n_informative=8,
                           class_sep=0.9, random_state=3)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, random_state=3, stratify=y)

modeles = {
    "logistique": LogisticRegression(max_iter=2000),
    "knn-11": Pipeline([("sc", StandardScaler()), ("m", KNeighborsClassifier(11))]),
    "arbre-prof-3": DecisionTreeClassifier(max_depth=3, random_state=0),
}
for nom, m in modeles.items():
    cv = cross_val_score(m, X_tr, y_tr, cv=5, scoring="roc_auc")
    print(f"{nom:15s} AUC = {cv.mean():.3f} (±{cv.std():.3f})")
```

### ✅ Quiz
1. Que fait la sigmoïde et pourquoi est-elle nécessaire en classification ?
2. Différence entre Ridge et Lasso ?
3. Pourquoi k-NN exige-t-il la normalisation ?
4. Qu'est-ce que le gain d'information dans un arbre ?
5. Quel modèle choisirais-tu pour un comité de crédit qui exige d'expliquer chaque décision ? (Réponse : logistique ou arbre peu profond.)

### 🛠️ Exercices
1. Sur un dataset réel **tabulaire**, compare logistique / k-NN / arbre peu profond / arbre profond en CV 5-folds. Tableau de résultats + 3 lignes de conclusion.
2. Fais varier `alpha` (Ridge) de 0,001 à 100 sur une régression : trace la courbe du R² de validation. Où est le bon réglage ?
3. Entraîne un arbre de profondeur 2, 3, 5, 10, None et observe l'écart train/test. Explique l'overfitting avec **tes** chiffres.
4. Visualise un arbre avec `plot_tree` et **écris l'arbre en français** (sous forme de règles « si… alors… »).

---

# CHAPITRE 11 — Arbres d'ensemble : Random Forest et Gradient Boosting

### 🎯 Objectif
Maîtriser les modèles qui **gagnent les compétitions et les entretiens** sur les données tabulaires. C'est ton meilleur atout pour un premier emploi junior.

### 💡 L'essentiel en 5 minutes

- **Random Forest** : on plante **des centaines d'arbres** différents (chacun sur un échantillon aléatoire de lignes et de colonnes), puis **on vote**. Résultat : beaucoup plus stable qu'un arbre seul.
- **Gradient Boosting (XGBoost / LightGBM / CatBoost)** : les arbres se construisent **en séquence**, chacun corrigeant les erreurs du précédent. C'est souvent le plus précis sur données tabulaires.

Analogie :
- Forêt = **un jury** qui vote (chaque juré a vu une partie du dossier).
- Boosting = **un étudiant qui retravaille uniquement ses fautes**, encore et encore.

### 📘 Le cours

#### 11.1 Bagging, Random Forest, ExtraTrees
- **Bagging (Bootstrap Aggregating)** : chaque arbre apprend sur un tirage **avec remise** des lignes.
- **Random Forest** ajoute : à chaque nœud, seules une **sous-partie aléatoire des colonnes** est considérée (réduit la corrélation entre arbres).
- **ExtraTrees** : seuils choisis aléatoirement → plus rapide, un peu plus biaisé.

Hyperparamètres clés :
| Paramètre | Rôle | Valeur de départ |
|---|---|---|
| `n_estimators` | nombre d'arbres | 300-500 (plus = mieux, jusqu'à un plateau) |
| `max_depth` | profondeur | None (grand) mais `min_samples_leaf` limite |
| `min_samples_leaf` | taille minimale d'une feuille | 1-20 (augmente si overfit) |
| `max_features` | colonnes par nœud | "sqrt" (valeur par défaut, efficace) |
| `class_weight` | déséquilibre | "balanced" si nécessaire |

```python
from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(n_estimators=400, min_samples_leaf=3,
                            class_weight="balanced", n_jobs=-1, random_state=42).fit(X_tr, y_tr)
print(rf.feature_importances_)   # importance des variables (à utiliser avec SHAP, cf. ch.13)
```
⚠️ **`oob_score=True`** donne une estimation « gratuite » de performance (échantillons hors-bag).

#### 11.2 Gradient Boosting : comment ça marche vraiment
À chaque étape, on ajoute un arbre qui apprend à **prédire les erreurs résiduelles** du modèle courant. Concrètement :
$$\hat y^{(t)} = \hat y^{(t-1)} + \eta \cdot h_t(x)$$
où $h_t$ est le nouvel arbre et $\eta$ le **learning rate** (ex. 0,05). Petit η = plus précis mais besoin de plus d'arbres.

**Les 3 bibliothèques à connaître :**
| Bibliothèque | Force | Astuce |
|---|---|---|
| **XGBoost** | référence historique, robuste | `learning_rate`, `max_depth`, `subsample`, `colsample_bytree` |
| **LightGBM** | **le plus rapide** sur gros volumes | idéal en production, très utilisé en entreprise |
| **CatBoost** | gère nativement les **colonnes catégorielles** | excellent sans prétraitement lourd |

```python
# pip install xgboost lightgbm catboost
from lightgbm import LGBMClassifier
gb = LGBMClassifier(n_estimators=600, learning_rate=0.05, num_leaves=31,
                    subsample=0.8, colsample_bytree=0.8, random_state=42)
gb.fit(X_tr, y_tr)
```

**Early stopping** (indispensable) :
```python
gb.fit(X_tr, y_tr, eval_set=[(X_val, y_val)],
       eval_metric="auc", callbacks=None)   # LightGBM : callbacks=[lgb.early_stopping(50)]
```
On arrête quand la performance de validation ne s'améliore plus → gain de temps et anti-overfitting.

#### 11.3 Quel modèle choisir ? (arbre de décision pratique)
```
Données tabulaires ?
├── Petites données (<10k lignes) et besoin d'explication  → logistique / arbre / RF
├── Beaucoup de colonnes catégorielles                     → CatBoost
├── Gros volumes, besoin de vitesse                        → LightGBM
├── Objectif : gagner le dernier point d'AUC               → XGBoost/LightGBM + réglage fin
└── Il faut expliquer à un régulateur                      → logistique + SHAP
```

#### 11.4 Stacking et ensembles (pour aller plus loin)
On combine les prédictions de plusieurs modèles avec un **méta-modèle** (souvent une logistique). `sklearn.ensemble.StackingClassifier`. À connaître de nom : c'est le dernier étage des solutions de compétition Kaggle.

### ⚠️ Les 3 erreurs classiques
1. **Croire que le boosting est toujours meilleur.** Sur petites données ou bruitées, la logistique peut gagner (et se déploie mieux).
2. **Chercher le dernier 0,1 % d'AUC** au lieu d'améliorer les **données** (nouvelles variables = plus gros gain presque toujours).
3. **Oublier que les modèles à base d'arbres gèrent mal les tendances temporelles** (ils n'extrapolent pas). Pour du temps, fabrique des variables de décalage (*lags*) et/ou utilise des modèles de séries temporelles.

### 💻 Code du chapitre
```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

X, y = make_classification(n_samples=3000, n_features=20, n_informative=10,
                           flip_y=0.08, random_state=7)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, random_state=7, stratify=y)

for nom, m in [("logistique", LogisticRegression(max_iter=2000)),
               ("random forest", RandomForestClassifier(n_estimators=400, n_jobs=-1, random_state=7))]:
    m.fit(X_tr, y_tr)
    print(f"{nom:15s} train AUC = {roc_auc_score(y_tr, m.predict_proba(X_tr)[:,1]):.3f} | "
          f"test AUC = {roc_auc_score(y_te, m.predict_proba(X_te)[:,1]):.3f}")
```
**Observation attendue** : la forêt a un score train presque parfait (signe d'overfitting interne) mais son score test reste bon. Commente cet écart : c'est exactement ce qu'un recruteur veut entendre.

### ✅ Quiz
1. Différence entre bagging et boosting ?
2. Pourquoi une forêt est-elle plus stable qu'un arbre seul ?
3. Que fait `learning_rate` dans le boosting ?
4. Quand préférer CatBoost ?
5. Pourquoi les modèles d'arbres sont-ils mauvais pour extrapoler une tendance temporelle ?

### 🛠️ Exercices
1. Sur un dataset tabulaire réel, compare logistique / RF / LightGBM / XGBoost en CV 5-folds (temps d'entraînement inclus). Tableau + conclusion en 5 lignes.
2. Fais varier `learning_rate` (0,3 / 0,1 / 0,05 / 0,01) avec early stopping. Note le nombre d'itérations optimal et l'AUC. Que constates-tu ?
3. Régression : entraîne un `RandomForestRegressor` et un `LGBMRegressor` sur un prix, compare MAE et RMSE à la baseline « prédire la moyenne ».
4. **Projet fil rouge** : passe au boosting, note le gain par rapport à ta logistique, et vérifie qu'aucune fuite n'a été introduite.

---

# CHAPITRE 12 — Non supervisé : regrouper, réduire, détecter

### 🎯 Objectif
Savoir segmenter des données, réduire la dimension pour visualiser, et détecter les anomalies.

### 💡 L'essentiel en 5 minutes

- **k-means** : on choisit k centres, chacun attire les points les plus proches → groupes homogènes.
- **CAH (clustering hiérarchique)** : on construit un arbre de regroupements (dendrogramme).
- **DBSCAN** : regroupe les points **denses** et isole le reste → détecte les anomalies et les formes non sphériques.
- **ACP (PCA)** : compresse 50 colonnes en 3 sans perdre trop d'information → pour visualiser et accélérer.

### 📘 Le cours

#### 12.1 k-means, algorithme exact
1. Choisir k (nombre de groupes).
2. Placer k centres au hasard (ou avec k-means++).
3. **Affectation** : chaque point rejoint le centre le plus proche.
4. **Mise à jour** : chaque centre devient la moyenne de son groupe.
5. Répéter 3-4 jusqu'à stabilisation.

Il minimise l'**inertie** : $\sum_k \sum_{x \in C_k} \|x - \mu_k\|^2$.

⚠️ **Toujours normaliser avant k-means** ; sinon une colonne en euros (millions) écrase une colonne en années.

**Choisir k :**
- **Méthode du coude** : tracer l'inertie selon k, chercher le « coude ».
- **Silhouette** (de -1 à 1, plus haut = mieux séparé).
- **Validation métier** : est-ce que les groupes ont un sens pour le client ? (le critère décisif !)

```python
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

Xs = StandardScaler().fit_transform(X)
for k in range(2, 9):
    km = KMeans(n_clusters=k, n_init=10, random_state=0).fit(Xs)
    print(k, round(km.inertia_), round(silhouette_score(Xs, km.labels_), 3))
```

#### 12.2 Clustering hiérarchique (CAH)
- **Agglomératif** : chaque point est un groupe ; on fusionne les deux groupes les plus proches, jusqu'à un seul.
- **Dendrogramme** : arbre montrant l'ordre des fusions ; on coupe où la « hauteur » saute.
- **Liaison** : `ward` (par défaut, donne des groupes compacts), `complete`, `average`, `single`.
- **Usage pro** : analyse de gènes, segmentation marketing avec peu d'observations.

#### 12.3 DBSCAN (et HDBSCAN)
- Paramètres : `eps` (rayon) et `min_samples` (densité minimale).
- Points isolés → **bruit** (label −1) = détection d'anomalies gratuite.
- Ne demande pas de choisir k, trouve des formes arbitraires, mais est **sensible à `eps`**.
- Homme de la détection d'anomalies industrielle/fraude.

#### 12.4 PCA / réduction de dimension
- Trouve des **axes** (composantes) qui maximisent la variance expliquée.
- Chaque composante est une **combinaison linéaire** des variables d'origine.
- On garde les composantes dont la **variance expliquée cumulée ≈ 90 %**.
```python
from sklearn.decomposition import PCA
pca = PCA(n_components=0.9).fit(Xs)
print("Composantes retenues :", pca.n_components_)
print("Variance expliquée :", pca.explained_variance_ratio_.round(3))
```
**À quoi ça sert vraiment ?** : visualiser en 2D/3D, débruiter, accélérer l'entraînement, éviter la multicolinéarité. **Ça ne sert pas** à « faire joli » en entretien : savoir dire *pourquoi* on l'utilise est ce qui compte.

**t-SNE / UMAP** : pour la visualisation 2D **uniquement** (ne pas utiliser comme features d'un modèle prédictif sans précaution).

#### 12.5 Détection d'anomalies (application très recherchée en Afrique et ailleurs)
- **Statistique** : z-score (>3), IQR.
- **Distance** : Isolation Forest, Local Outlier Factor.
- **Densité** : DBSCAN.
- **Cas d'usage** : fraudes Mobile Money, pannes d'équipement, fuites d'eau, compteurs électriques, transactions bancaires.

### ⚠️ Les 3 erreurs classiques
1. **Interpréter k-means sans normaliser.**
2. **Croire que les clusters sont « vrais »** : ce sont des hypothèses, à valider avec le métier.
3. **Utiliser PCA puis interpréter les composantes comme des variables d'origine** (ce sont des mélanges).

### 💻 Code du chapitre
```python
import numpy as np
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

X = StandardScaler().fit_transform(load_iris().data)
km = KMeans(n_clusters=3, n_init=10, random_state=0).fit(X)
print("Silhouette k-means :", round(silhouette_score(X, km.labels_), 3))

db = DBSCAN(eps=0.9, min_samples=5).fit(X)
print("Clusters DBSCAN :", set(db.labels_), "| anomalies :", (db.labels_ == -1).sum())

p = PCA(n_components=2).fit_transform(X)
print("Forme après PCA :", p.shape)
```

### ✅ Quiz
1. Pourquoi normaliser avant k-means ?
2. Que mesure la silhouette ?
3. Quel avantage a DBSCAN sur k-means ?
4. Que signifie « variance expliquée à 90 % » pour une PCA à 4 composantes ?
5. Quelle méthode utiliserais-tu pour détecter des transactions Mobile Money suspectes ?

### 🛠️ Exercices
1. Segmente un dataset client (ou les données de consommation d'électricité d'un quartier) en k=3..6, choisis le k, **nomme chaque segment** en français (« jeunes urbains dépensiers »…) et propose une action marketing par segment.
2. Utilise Isolation Forest sur un dataset avec anomalies injectées ; calcule combien tu en retrouves (rappel).
3. Fais une PCA sur un dataset à >10 colonnes, trace les 2 premières composantes colorées par classe.

---

# CHAPITRE 13 — Projet ML complet + interprétabilité (le chapitre qui décroche l'entretien)

### 🎯 Objectif
Livrer **un projet complet, propre, expliqué** : c'est ta preuve de compétence. Les recruteurs (France, Belgique, Suisse, Québec) accordent plus de poids à 2 projets finis qu'à 10 notebooks bâclés.

### 💡 L'essentiel en 5 minutes

Un projet qui impressionne n'est pas un projet « avancé » : c'est un projet **cadré, mesuré, expliqué et reproductible**. La structure ci-dessous vaut pour tous tes projets à venir.

### 📘 Le cours

#### 13.1 La structure d'un projet professionnel
```
mon-projet/
├── README.md            ← la vitrine : problème, données, résultat, comment lancer
├── requirements.txt     ← versions des libs (reproductibilité)
├── data/raw/            ← données brutes (jamais modifiées)
├── data/processed/      ← données transformées
├── notebooks/
│   ├── 01_exploration.ipynb
│   ├── 02_modele.ipynb
│   └── 03_evaluation.ipynb
├── src/
│   ├── data.py          ← chargement + nettoyage (fonctions réutilisables)
│   ├── features.py      ← création des variables
│   ├── train.py         ← entraînement + sauvegarde du modèle
│   └── predict.py       ← prédiction sur nouvelles données
├── models/modele.pkl    ← modèle sérialisé (joblib)
└── reports/figures/     ← graphiques pour le README
```

#### 13.2 Le README qui fait la différence (modèle à copier)
```markdown
# Prédiction du risque de défaut de paiement — Burkina Faso
## Problème business
Une institution de microfinance veut réduire ses pertes en anticipant les défauts.
Objectif : identifier 80 % des défauts en limitant les fausses alertes à 20 % du portefeuille.
## Données
12 400 dossiers de crédit (2019-2025), 24 variables. Source : [lien]. Nettoyage documenté dans `notebooks/01`.
## Méthode
1. Baseline : règle métier « impayé > 30 jours dans les 6 derniers mois » → rappel 0,41
2. Logistic Regression (interprétable) → AUC 0,74
3. LightGBM + réglage → **AUC 0,81, rappel 0,63 @ seuil 0,42**
## Résultat business
Au seuil retenu : 63 % des défauts détectés, soit une économie estimée à X FCFA/an.
## Limites et suite
Dérive possible si les conditions économiques changent (surveillance mensuelle prévue)…
## Reproduire
python src/train.py --data data/raw/dossiers.csv
```

#### 13.3 L'interprétabilité : SHAP (le recruteur adore)
Les importances de variables de sklearn ne disent pas **le sens** ni **pour qui**. **SHAP** donne, pour **chaque prédiction**, la contribution de chaque variable.
```python
# pip install shap
import shap
explainer = shap.Explainer(modele.predict_proba, X_tr)   # pour un pipeline sklearn
shap_values = explainer(X_te[:200])
shap.plots.beeswarm(shap_values)          # vue globale : quelles variables pèsent
shap.plots.waterfall(shap_values[0])      # vue individuelle : pourquoi CE dossier a été refusé
```
**Argument en entretien** : « Je peux expliquer chaque décision individuellement, et pas seulement dire que le modèle est bon en moyenne » — c'est ce qui distingue un junior pro d'un junior scolaire, et c'est **exigé par le RGPD** (droit à l'explication) en Europe.

#### 13.4 Ingénierie de variables (là où se gagnent les points)
| Technique | Exemple |
|---|---|
| Ratios | montant_crédit / revenu_mensuel |
| Agrégats par groupe | moyenne des retards par agence |
| Temporel | jour de la semaine, mois, jours depuis le dernier incident, *lags* |
| Texte simple | longueur, nombre de mots, présence de mots-clés |
| Catégoriel | fréquence d'apparition, cible moyenne (⚠️ à calculer **dans** la CV) |
| Interactions | budget × ancienneté |

**Test A/B de features** : ajoute une variable, mesure le gain en CV. Si le gain < bruit (≈ 0,005 AUC), garde le modèle simple.

#### 13.5 La checklist finale avant de dire « c'est fini »
- [ ] Aucune fuite (vérifié avec la liste du chapitre 8.2).
- [ ] Test touché une seule fois, à la fin, et c'est ce score que j'annonce.
- [ ] Baseline battue, et je peux le prouver.
- [ ] Le modèle est sauvegardé et rechargeable (`joblib.dump` / `joblib.load`).
- [ ] `requirements.txt` + README avec instructions de reproduction.
- [ ] 3 graphiques clairs, légendés, avec les unités.
- [ ] Une section **limites** (honnêteté = maturité professionnelle).
- [ ] Communication d'une page pour un non-technique (moins de jargon possible).

### ⚠️ Les 3 erreurs classiques
1. **Projet Titanic/Iris** comme vitrine → tout le monde l'a fait. Choisis **ton** problème (agriculture sahélienne, énergie, santé, mobile money).
2. **AUC annoncée sans contexte business** → le recruteur veut un impact, pas un chiffre.
3. **Pas de README** → même un excellent modèle paraîtra amateur.

### 🛠️ Exercice final de la Partie 2 (2 à 4 semaines)
Réalise **ton projet ML complet** avec les thèmes possibles :
- prédiction du prix des céréales ou du bétail ;
- prédiction de la consommation d'électricité / d'eau ;
- détection de fraude Mobile Money ;
- prédiction de l'abandon scolaire ;
- recommandation de cultures selon météo et sol.

Livrable : dépôt GitHub + README structuré + notebook + modèle `.pkl` + 3 graphiques + section limites.

---

## 🏁 Fin de la Partie 2 : auto-évaluation

Tu es prêt pour la Partie 3 (Deep Learning) si tu peux :
- [ ] expliquer la différence entre biais et variance, avec un exemple chiffré ;
- [ ] citer 4 formes de data leakage et les éviter avec un Pipeline ;
- [ ] choisir la bonne métrique selon le coût des erreurs ;
- [ ] comparer 4 modèles avec cross-validation et justifier ton choix ;
- [ ] interpréter un modèle avec SHAP et le raconter en 3 phrases à un non-technique ;
- [ ] montrer **un projet complet** sur GitHub avec README professionnel.

**C'est ici que se joue ton employabilité.** Beaucoup de candidats parlent de deep learning ; peu savent livrer un projet tabulaire propre. Ne saute pas cette partie.

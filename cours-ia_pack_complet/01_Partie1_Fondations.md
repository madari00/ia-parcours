# PARTIE 1 — FONDATIONS : coder, calculer, comprendre

> **Durée prévue :** semaines 1 à 12 (5-10 h/semaine)
> **Objectif de fin de partie :** tu sais écrire un programme Python propre, manipuler des données avec NumPy/Pandas, et tu comprends *vraiment* les 3 maths de l'IA (vecteurs, dérivées, probabilités).

---

## 🧭 Comment cette partie est organisée

| Chapitre | Sujet | Semaines |
|---|---|---|
| 0 | La méthode d'apprentissage qui marche | 1 |
| 1 | Python essentiel | 1-4 |
| 2 | NumPy : les maths qui calculent vite | 4-5 |
| 3 | Pandas : lire et nettoyer des données | 5-7 |
| 4 | Maths 1 : vecteurs et matrices | 7-9 |
| 5 | Maths 2 : dérivées et descente de gradient | 9-10 |
| 6 | Maths 3 : probabilités et statistiques | 10-12 |

---

# CHAPITRE 0 — La méthode (le chapitre le plus important)

### 🎯 Objectif
Savoir *comment* apprendre pour ne pas abandonner au mois 2 (le mois où 80 % des autodidactes abandonnent).

### 💡 L'essentiel en 5 minutes

Ton cerveau n'apprend pas en lisant, il apprend en **récupérant** l'information (en se forçant à se souvenir). Trois techniques suffisent :

1. **La pratique active** : après chaque section, ferme le document et écris le code de mémoire.
2. **L'espacement (spaced repetition)** : révise à J+1, J+3, J+7, J+21. Note tes 5 notions du jour dans un carnet, relis-les le lendemain.
3. **Le projet fil rouge** : choisis **UNE** problématique qui te tient à cœur (ex. : *prédire les prix des céréales au Burkina* ou *détecter les maladies du mil par photo*). Tu la réutiliseras à chaque chapitre, en l'améliorant. À la fin, elle devient ton projet de portfolio.

### 📘 Le cours

**Pourquoi 80 % abandonnent :** ils suivent des vidéos (« je comprends tout ! ») sans jamais écrire de code seuls. La compréhension passive donne l'illusion du savoir. Le test réel : *« est-ce que je peux l'expliquer à quelqu'un avec mes mots et le coder sans regarder ? »*

**La règle des 30/70 :** 30 % lecture, 70 % clavier.

**Le cycle hebdomadaire (à répéter 52 fois) :**

| Jour | Activité | Durée |
|---|---|---|
| Lundi | Lire 1 ou 2 sections du cours + prendre des notes | 1 h |
| Mardi | Retaper les exemples de code *sans regarder* | 1 h |
| Mercredi | Faire les exercices du chapitre | 1 h |
| Jeudi | Corriger, comprendre chaque erreur, avancer le projet fil rouge | 1 h |
| Vendredi | Quiz à froid + révision espacée (carnet) | 30 min |
| Samedi | **Bloc projet** : 2 h sur ton projet ou un mini-défi | 2 h |
| Dimanche | Repos ou veille (lire un article, regarder une vidéo technique) | 30 min |

### ⚠️ Les 3 erreurs classiques
1. **Tutoriel-hopping** : changer de cours chaque semaine. → Fini celui-ci d'abord.
2. **Collectionner les certificats** sans projets. → Un certificat sans projet = papier.
3. **Vouloir tout comprendre à 100 % avant d'avancer.** → 80 % puis avance ; tu reviendras.

### ✅ Quiz
1. Quelle proportion du temps doit passer au clavier ? 
2. Cite 2 jours où tu feras de la révision espacée.
3. Vrai ou faux : « si je comprends en regardant la vidéo, je sais faire ».
4. Pourquoi un projet fil rouge unique est-il supérieur à 10 mini-exercices ?
5. Quelles sont tes 2 heures fixes de la semaine ? (Écris-les maintenant.)

*(Réponses à la fin du chapitre.)*

### 🛠️ Exercice (30 min)
Crée un fichier `carnet.md` avec 3 sections : **Notions du jour**, **Erreurs du jour**, **Idée de projet**. Remplis-le aujourd'hui. Ouvre un compte GitHub et pousse ce fichier.

---

# CHAPITRE 1 — Python essentiel

### 🎯 Objectif
Écrire des programmes Python clairs : variables, conditions, boucles, fonctions, listes, dictionnaires, fichiers, gestion d'erreurs, modules, classes simples, et utiliser Git.

### 💡 L'essentiel en 5 minutes

Un programme = **des données** + **des instructions**. On stocke les données dans des *variables*, on décide avec `if`, on répète avec `for`/`while`, on regroupe des instructions dans des *fonctions*, on range des ensembles de valeurs dans des *listes* et des *dictionnaires*.

### 📘 Le cours

#### 1.1 Variables et types
Une variable est une **étiquette collée sur une boîte**. La boîte contient une valeur.

```python
nom = "Awa"          # str  (texte)
age = 24             # int  (entier)
taille = 1.72        # float (décimal)
etudiant = True      # bool (vrai/faux)
notes = [12, 15, 9]  # list (liste ordonnée)
infos = {"ville": "Ouagadougou", "pays": "BF"}  # dict (clé → valeur)
```

**Règle :** les noms de variables s'écrivent en `minuscules_avec_underscores`, jamais `x1`, `truc2`.

#### 1.2 Conditions
```python
note = 14
if note >= 16:
    mention = "très bien"
elif note >= 12:
    mention = "bien"
else:
    mention = "passable"
print(mention)   # bien
```
Le `:` et l'**indentation** (4 espaces) ne sont pas décoratifs : ils délimitent les blocs en Python.

#### 1.3 Boucles
```python
for note in [12, 15, 9]:
    print("Note :", note)

for i in range(3):      # i = 0, 1, 2
    print(i)

total = 0
k = 1
while k <= 5:           # tant que la condition est vraie
    total += k
    k += 1
print(total)            # 15
```
⚠️ `for` quand tu connais la collection, `while` quand tu répètes *jusqu'à* ce qu'une condition change.

#### 1.4 Fonctions
Une fonction = **une recette réutilisable**.
```python
def moyenne(notes):
    """Renvoie la moyenne d'une liste de notes."""
    return sum(notes) / len(notes)

print(moyenne([12, 15, 9]))   # 12.0
```
- `def` = « je définis ».
- Les parenthèses contiennent les **paramètres** (les entrées).
- `return` = la **sortie**. Sans `return`, la fonction renvoie `None`.

#### 1.5 Listes, dictionnaires, comprehensions
```python
notes = [8, 12, 17, 11]
notes.append(20)                 # ajouter à la fin
notes[0]                        # 8  (index commence à 0)
notes[-1]                       # 20 (dernier)
notes[1:3]                      # [12, 17] (tranche : index 1 inclus → 3 exclus)

# « comprehension » : construire une liste en une ligne
notes_20 = [n / 20 for n in notes]          # normaliser entre 0 et 1
bonnes = [n for n in notes if n >= 12]      # filtrer
print(bonnes)   # [12, 17, 20]

eleve = {"nom": "Awa", "notes": [12, 15, 9]}
eleve["notes"].append(18)
for cle, valeur in eleve.items():
    print(cle, "→", valeur)
```

#### 1.6 Gestion d'erreurs
En IA, les données sont sales : un fichier manquant, un texte à convertir en nombre... Un bon code **prévient** au lieu de planter.
```python
def to_float(texte):
    try:
        return float(texte)
    except ValueError:
        return None          # ou une valeur par défaut

print(to_float("12.5"))   # 12.5
print(to_float("abc"))    # None
```

#### 1.7 Modules et fichiers
```python
import math, json, os

math.sqrt(16)            # 4.0

# écrire un fichier JSON (format standard pour sauvegarder des résultats)
resultats = {"modele": "linear", "score": 0.87}
with open("resultats.json", "w", encoding="utf-8") as f:
    json.dump(resultats, f, ensure_ascii=False, indent=2)

# relire
with open("resultats.json", encoding="utf-8") as f:
    data = json.load(f)
print(data["score"])     # 0.87
```
⚠️ `with open(...)` ferme le fichier automatiquement : **toujours** l'utiliser.

#### 1.8 Classes (l'essentiel seulement)
Une classe = **un moule** ; un objet = **une pièce fabriquée avec ce moule**. Sert à regrouper données + comportements (utile quand tu coderas tes propres modèles).
```python
class Eleve:
    def __init__(self, nom):
        self.nom = nom          # self = « cet objet-là »
        self.notes = []

    def ajouter_note(self, note):
        self.notes.append(note)

    def moyenne(self):
        return sum(self.notes) / len(self.notes) if self.notes else 0

a = Eleve("Awa")
a.ajouter_note(15); a.ajouter_note(11)
print(a.nom, a.moyenne())      # Awa 13.0
```

#### 1.9 Git et GitHub (indispensable pour l'Occident)
```bash
git init                          # démarrer un dépôt
git add .                         # préparer les fichiers
git commit -m "feat: premier commit"    # enregistrer
git branch -M main
git remote add origin https://github.com/TON_PSEUDO/mon-projet.git
git push -u origin main
```
**Messages de commit utiles** : `feat: ajoute le chargement des données`, `fix: corrige le calcul de la moyenne`, `docs: met à jour le README`. Jamais `update` ou `test`.

Un fichier `.gitignore` doit contenir au minimum : `__pycache__/`, `.ipynb_checkpoints/`, `*.csv` (si données lourdes), `models/*.pth`, `.env`.

### ⚠️ Les 3 erreurs classiques
1. **Oublier d'indenter** ou mélanger tabulations et espaces → `IndentationError`.
2. **Modifier la liste qu'on parcourt** → comportement imprévisible. Fais une copie : `for n in notes.copy():`.
3. **Nommer une variable `list`, `sum`, `str`** → tu écrases une fonction Python.

### 💻 Code du chapitre (à retaper sans regarder)
```python
def statistiques(notes):
    if not notes:
        return {"n": 0, "moyenne": None, "min": None, "max": None}
    return {
        "n": len(notes),
        "moyenne": round(sum(notes) / len(notes), 2),
        "min": min(notes),
        "max": max(notes),
    }

assert statistiques([12, 15, 9]) == {"n": 3, "moyenne": 12.0, "min": 9, "max": 15}
print(statistiques([]))
```

### ✅ Quiz
1. Différence entre `for` et `while` ?
2. Que fait `notes[1:3]` ?
3. Que renvoie une fonction sans `return` ?
4. Pourquoi `with open(...)` plutôt que `open(...)` seul ?
5. Écris en une ligne la liste des carrés des nombres de 1 à 5. *(réponse : `[i**2 for i in range(1, 6)]`)*

### 🛠️ Exercices
1. **Convertisseur** : fonction `fcfa_vers_euro(montant)` (1 € = 655,957 FCFA), arrondie à 2 décimales.
2. **Analyse de texte** : compte le nombre de mots d'un texte et renvoie les 3 mots les plus fréquents (indice : `split()`, `.lower()`, dictionnaire).
3. **Fichier** : lis une liste de notes depuis un fichier texte (une note par ligne), écris un JSON avec les statistiques.
4. **Git** : crée un dépôt `ia-parcours`, ajoute tes 3 programmes, un README de 10 lignes, pousse sur GitHub.

*Réponses du quiz : 1) 70 % – 2) vendredi + dispatching à J+1/J+3/J+7 – 3) faux – 4) parce qu'on approfondit un vrai problème et qu'il devient une preuve de compétence – 5) réponse personnelle.*

---

# CHAPITRE 2 — NumPy : les maths qui calculent vite

### 🎯 Objectif
Manipuler des vecteurs et matrices en Python, comprendre les `shape`, le broadcasting, et pourquoi on « vectorise » au lieu de faire des boucles.

### 💡 L'essentiel en 5 minutes

Un réseau de neurones fait des **milliards** de multiplications. En Python pur, une boucle est ~100 fois plus lente que NumPy. **NumPy = calcul sur des tableaux entiers d'un coup**, écrit en C sous le capot.

Analogies :
- **Tableau 1D** = une ligne de cases (un vecteur).
- **Tableau 2D** = une grille, comme un tableau Excel (une matrice).
- **shape** = `(lignes, colonnes)`. `(150, 4)` = 150 exemples, 4 caractéristiques.
- **Broadcasting** = « NumPy étire automatiquement la petite forme pour qu'elle s'aligne sur la grande ».

### 📘 Le cours

```python
import numpy as np

a = np.array([1, 2, 3])              # vecteur, shape (3,)
M = np.array([[1, 2], [3, 4], [5, 6]])  # matrice 3x2
print(M.shape)                       # (3, 2)
print(M.ndim)                        # 2 dimensions
print(a.dtype)                       # int64
```

#### 2.1 Créer des tableaux
```python
np.zeros((2, 3))          # matrice de 0
np.ones(4)                # vecteur de 1
np.arange(0, 10, 2)       # [0 2 4 6 8]  (début, fin exclue, pas)
np.linspace(0, 1, 5)      # [0. 0.25 0.5 0.75 1.] (5 points équidistants)
np.random.default_rng(42).normal(0, 1, size=(3, 2))   # aléatoire reproductible
```
⚠️ **Toujours** fixer la graine (`seed`) : `rng = np.random.default_rng(42)`. Sans ça, tes résultats changent à chaque exécution — impossible de déboguer.

#### 2.2 Indexation et filtrage booléen
```python
x = np.array([10, 20, 30, 40, 50])
x[0], x[-1]          # 10, 50
x[1:4]               # [20 30 40]
x[x > 25]            # [30 40 50]   ← filtre booléen, très utilisé
(x > 25).sum()       # 3  (nombre d'éléments qui satisfont la condition)
M[0, 1]              # ligne 0, colonne 1
M[:, 0]              # toute la première colonne
```

#### 2.3 Opérations élément par élément (vectorisation)
```python
a = np.array([1, 2, 3])
b = np.array([10, 20, 30])
a + b          # [11 22 33]
a * 2          # [2 4 6]
a ** 2         # [1 4 9]
np.sqrt(a)     # [1. 1.41 1.73]
a.mean(), a.sum(), a.max()
```
**Pas de boucle !** `[x*2 for x in a]` est correct mais 50 à 100× plus lent sur de gros volumes.

#### 2.4 Broadcasting
```python
X = np.array([[1, 2, 3],
              [4, 5, 6]])       # shape (2, 3)
moyenne = X.mean(axis=0)         # shape (3,) → colonne par colonne : [2.5 3.5 4.5]
Xc = X - moyenne                 # (2,3) - (3,) → NumPy étire sur les lignes
print(Xc)
# [[-1.5 -1.5 -1.5]
#  [ 1.5  1.5  1.5]]
```
Règle de compatibilité : les dimensions, lues **de droite à gauche**, doivent être égales ou valoir 1. Ici `3` face à `3` : OK.
`axis=0` = « je descends le long des lignes » (résultat par colonne). `axis=1` = par ligne.

#### 2.5 Produit matriciel
```python
A = np.array([[1, 2], [3, 4]])   # (2,2)
v = np.array([5, 6])             # (2,)
A @ v                            # [17 39]  ← opérateur @ (produit matriciel)
```
`(2,2) @ (2,) → (2,)`. La règle : les dimensions **intérieures** doivent s'accorder : `(n, m) @ (m, p) → (n, p)`.

#### 2.6 Normalisation (recette à connaître par cœur)
```python
def normaliser(X):
    """Centre à 0 et réduit l'écart-type à 1 (moyenne 0, écart-type 1)."""
    return (X - X.mean(axis=0)) / (X.std(axis=0) + 1e-8)  # +1e-8 évite la division par 0
```

### ⚠️ Les 3 erreurs classiques
1. **Confondre `*` (élément par élément) et `@` (produit matriciel)** → résultats silencieusement faux.
2. **Se tromper de `axis`** : `axis=0` → résultat de taille (nb colonnes).
3. **Oublier `dtype`** : `np.array([1,2,3]) / 2` donne des floats — parfois tu voulais des entiers ; sois explicite.

### 💻 Code du chapitre
```python
import numpy as np

rng = np.random.default_rng(0)
X = rng.normal(size=(100, 3))
Xn = normaliser(X)
assert np.allclose(Xn.mean(axis=0), 0, atol=1e-6)
assert np.allclose(Xn.std(axis=0), 1, atol=1e-6)
print("Normalisation OK", Xn.shape)
```

### ✅ Quiz
1. `shape` de `np.zeros((4, 2))` ? Et son `ndim` ?
2. Que vaut `np.arange(1, 6) ** 2` ?
3. Pourquoi `X - X.mean(axis=0)` fonctionne-t-il malgré des formes différentes ?
4. `(100, 4) @ (4, 3)` donne quelle forme ?
5. Pourquoi fixer la graine aléatoire ?

### 🛠️ Exercices
1. Crée une matrice `(5, 3)` de notes aléatoires entre 0 et 20, calcule la moyenne par étudiant (axis=1) et par matière (axis=0).
2. Normalise une matrice de 200 lignes × 5 colonnes et vérifie que chaque colonne a une moyenne ≈ 0.
3. Calcule la distance euclidienne entre deux vecteurs sans boucle : `np.sqrt(((a-b)**2).sum())`.
4. **Projet fil rouge** : charge tes premières données réelles (CSV de Kaggle ou data.gouv.fr) dans un tableau NumPy, affiche `shape`, `mean`, `std`, et compte les valeurs manquantes avec `np.isnan(X).sum()`.

---

# CHAPITRE 3 — Pandas : lire et nettoyer des données

### 🎯 Objectif
Charger un CSV, explorer un jeu de données, filtrer, grouper, fusionner, gérer les valeurs manquantes.

### 💡 L'essentiel en 5 minutes

> **80 % du travail d'un data scientist/IA, c'est nettoyer et préparer les données.** Le modèle, c'est les 20 % restants.

Pandas, c'est **Excel en code** : un `DataFrame` = un tableau avec des noms de colonnes, des index, et des milliers d'opérations en une ligne.

### 📘 Le cours

#### 3.1 Charger et explorer (réflexe à automatiser)
```python
import pandas as pd

df = pd.read_csv("donnees.csv")
df.head()            # 5 premières lignes
df.shape             # (lignes, colonnes)
df.info()            # types + valeurs non nulles
df.describe()        # statistiques : moyenne, écart-type, min, quartiles, max
df["prix"].value_counts()      # fréquences des valeurs (colonnes catégorielles)
df.isna().sum()      # nombre de valeurs manquantes par colonne ← réflexe n°1
```

#### 3.2 Sélectionner
```python
df["prix"]                      # une colonne (Series)
df[["prix", "ville"]]           # plusieurs colonnes (DataFrame)
df.loc[0, "prix"]               # par étiquette/index
df.iloc[0, 2]                   # par position
df[df["prix"] > 100]            # filtre booléen
df[(df["ville"] == "Ouagadougou") & (df["prix"] > 100)]   # ET → &   OU → |
```

#### 3.3 Grouper et agréger (`groupby` = le couteau suisse)
```python
df.groupby("ville")["prix"].mean()
df.groupby("ville").agg({"prix": ["mean", "median", "count"], "quantite": "sum"})
```
Approche **split-apply-combine** : on découpe par ville → on calcule → on recolle le résultat.

#### 3.4 Créer / transformer
```python
df["prix_ttc"] = df["prix"] * 1.18
df["date"] = pd.to_datetime(df["date"])
df["mois"] = df["date"].dt.month
df["categorie"] = pd.cut(df["prix"], bins=[0, 100, 500, 10000],
                         labels=["bas", "moyen", "haut"])
```

#### 3.5 Fusionner (jointures)
```python
ventes = pd.DataFrame({"id_client": [1, 2, 3], "montant": [50, 200, 30]})
clients = pd.DataFrame({"id_client": [1, 2, 4], "ville": ["Ouaga", "Bobo", "Koudougou"]})
pd.merge(ventes, clients, on="id_client", how="left")
# how = "inner" (intersection) | "left" | "right" | "outer"
```

#### 3.6 Valeurs manquantes — les 3 stratégies
1. **Supprimer** : `df.dropna(subset=["cible"])` (si peu de lignes concernées **et** risque faible).
2. **Imputer** : `df["prix"] = df["prix"].fillna(df["prix"].median())` (médiane = robuste aux extrêmes).
3. **Indiquer** : créer une colonne `prix_manquant` (0/1) — parfois l'absence est *une information*.

```python
df = df.drop_duplicates()
df = df.sort_values("date")
```

#### 3.7 Le piège du « data leakage »
**Ne jamais** calculer une statistique (moyenne, médiane, encodage) sur l'ensemble des données avant de séparer train/test. Sinon le modèle « triche » : il connaît l'avenir. Règle : **on sépare d'abord, on calcule ensuite, mais on ajuste (`fit`) uniquement sur le train** — nous y reviendrons au chapitre ML.

### ⚠️ Les 3 erreurs classiques
1. **`df["col"] = ...` sur une copie** → `SettingWithCopyWarning` silencieux, modifications perdues. Utilise `df = df.copy()`.
2. **Comparer des types différents** (`"100" > 50`) → Pandas renvoie du bizarre ; convertis d'abord.
3. **Ignorer les valeurs manquantes** → le modèle plante ou produit des résultats faux.

### 💻 Code du chapitre (jeu de données intégré, fonctionne hors ligne)
```python
import pandas as pd

data = pd.DataFrame({
    "ville": ["Ouagadougou", "Bobo-Dioulasso", "Ouagadougou", "Koudougou", "Bobo-Dioulasso", None],
    "prix_kg": [450, 375, 500, 320, 390, 410],
    "quantite": [120, 80, 200, 60, 90, 30],
})
data["prix_kg"] = data["prix_kg"].fillna(data["prix_kg"].median())
resume = (data.groupby("ville")["prix_kg"]
              .agg(["mean", "median", "count"])
              .sort_values("mean", ascending=False))
print(resume)
print("Chiffre d'affaires total :", (data["prix_kg"] * data["quantite"]).sum())
```

### ✅ Quiz
1. Quelle commande donne le nombre de valeurs manquantes par colonne ?
2. Différence entre `loc` et `iloc` ?
3. Que fait `df.groupby("ville")["prix"].mean()` ?
4. Pourquoi imputer par la médiane plutôt que par la moyenne ?
5. Qu'est-ce que le data leakage, en une phrase ?

### 🛠️ Exercices
1. Crée un DataFrame de 20 lignes (ventes : date, ville, produit, quantité, prix). Calcule le CA par ville et par mois, trouve la meilleure ville.
2. Nettoie-le : 3 valeurs manquantes, 2 doublons, 1 prix négatif (à corriger ou signaler).
3. **Projet fil rouge** : télécharge un dataset public (Kaggle/meteo Burkina, prix agricoles, données de santé) et écris un notebook `exploration.ipynb` en 10 cellules : chargement → info → valeurs manquantes → 3 graphiques → 3 observations écrites en français.

### 📚 Ressources
- *10 minutes to pandas* (doc officielle, traduite en français) — à mettre en favori.
- Kaggle : cours « Pandas » (gratuit, ~4 h).
- France : data.gouv.fr ; Afrique : open.africa, HDX (données humanitaires Sahel).

---

# CHAPITRE 4 — Maths 1 : vecteurs, matrices, distances

### 🎯 Objectif
Comprendre les objets mathématiques que manipule tout modèle d'IA, sans jargon : vecteur, norme, produit scalaire, distance, matrice.

### 💡 L'essentiel en 5 minutes

**Un modèle d'IA transforme des nombres en d'autres nombres.** Pour ça, il faut :
- ranger les informations en **vecteurs** (une ligne de nombres = un exemple) ;
- mesurer la **ressemblance** entre deux vecteurs (produit scalaire, distance) ;
- appliquer des **transformations** (matrices).

C'est tout. Le reste, c'est de la combinaison de ces 3 idées.

### 📘 Le cours

#### 4.1 Vecteur
Un vecteur = **liste ordonnée de nombres**. Exemple : un client décrit par `[âge=35, revenu=250000, achats=12]`.

- **Dimension** : le nombre de coordonnées. Ici 3.
- **Norme (longueur)** : $\|x\| = \sqrt{x_1^2 + x_2^2 + \dots + x_n^2}$
  Exemple : `x = [3, 4]` → $\|x\| = \sqrt{9+16} = 5$.
- **Addition** : composante par composante. `[1,2] + [3,4] = [4,6]`.
- **Multiplication par un scalaire** : `2 × [1,2] = [2,4]` (la flèche s'allonge, même direction).

#### 4.2 Produit scalaire (l'opération reine de l'IA)
$$x \cdot y = x_1 y_1 + x_2 y_2 + \dots + x_n y_n$$

Exemple : `x = [1, 2, 3]`, `y = [4, 5, 6]` → `1×4 + 2×5 + 3×6 = 32`.

**Deux lectures complémentaires, à connaître :**
1. **Similitude** : plus le produit scalaire est grand (en valeurs absolues), plus les vecteurs pointent dans la même direction. C'est exactement ce qu'utilise un moteur de recherche (et un LLM) pour comparer deux textes transformés en vecteurs (embeddings).
2. **Brique de calcul** : un neurone fait `produit scalaire + biais`. Un réseau de neurones = des millions de produits scalaires.

Formule « géométrique » : $x \cdot y = \|x\|\,\|y\|\cos(\theta)$, où $\theta$ est l'angle entre les vecteurs.
- Produit scalaire = 0 → vecteurs **perpendiculaires** (indépendants).
- Cosinus = 1 → vecteurs **identiques en direction**.

#### 4.3 Similarité cosinus (très utilisée en NLP/RAG)
$$\text{sim}(x,y) = \frac{x \cdot y}{\|x\|\,\|y\|}$$
Elle vaut 1 (identiques), 0 (aucun rapport), -1 (opposés). Indépendante de la longueur → parfaite pour comparer des textes de tailles différentes.

#### 4.4 Distance euclidienne
$d(x,y) = \|x - y\| = \sqrt{\sum_i (x_i - y_i)^2}$
C'est la distance « à vol d'oiseau ». Utilisée en clustering (k-means) et en k-NN.

#### 4.5 Matrices
Une matrice = **un tableau 2D** de taille (n lignes, m colonnes). Interprétation en IA : **n exemples × m caractéristiques**.

**Produit matriciel** : $C = A B$, avec $C_{ij} = \sum_k A_{ik} B_{kj}$ (produit scalaire de la ligne *i* de A avec la colonne *j* de B).
Dimensions : `(n, m) @ (m, p) = (n, p)`.

Exemple :
```
A = [[1, 2],      B = [[1, 0],
     [3, 4]]           [0, 1]]
A @ B = A          (B est la matrice identité)
```

**Transposée** $A^T$ : on échange lignes et colonnes.
**Identité** $I$ : ne change rien ($AI = A$).
**Inverse** $A^{-1}$ : annule A ($A A^{-1} = I$). N'existe que si A est inversible — en pratique, on évite de la calculer (instable numériquement).

#### 4.6 Application directe : une régression linéaire en une ligne
Un modèle linéaire prédit $\hat{y} = X w + b$.
- `X` : (n, m) — les données
- `w` : (m,) — les poids (ce qu'on apprend)
- `b` : le biais
- `X @ w + b` → (n,) — une prédiction par exemple

C'est **littéralement** ce que fait NumPy dans le chapitre suivant : `X @ w + b`.

### ⚠️ Les 3 erreurs classiques
1. **Croire que `A @ B` = `B @ A`.** C'est faux en général (et parfois impossible : dimensions incompatibles).
2. **Confondre norme et somme.** La norme est une racine carrée.
3. **Oublier de normaliser avant de comparer.** Deux vecteurs peuvent avoir un produit scalaire énorme juste parce qu'ils sont *longs*.

### ✅ Quiz
1. Norme de `[6, 8]` ?
2. `[1,2,3] · [1,1,1]` ?
3. Si `sim_cos = 0`, que peut-on dire des deux textes ?
4. Forme du résultat de `(50, 10) @ (10, 1)` ?
5. Que représentent les lignes et les colonnes d'une matrice de données ?

### 🛠️ Exercices
1. Calcule à la main puis vérifie avec NumPy : norme de `[1,2,2]`, produit scalaire de `[2,0,1]` et `[1,3,2]`, et la similarité cosinus de ces deux vecteurs.
2. Prends 3 phrases, transforme-les en vecteurs de fréquences de mots (compte « ia », « data », « modèle »), calcule les similarités cosinus 2 à 2. Conclusion ?
3. Écris une fonction `predire(X, w, b)` qui renvoie `X @ w + b` et teste-la sur une matrice (4, 3).

---

# CHAPITRE 5 — Maths 2 : dérivées et descente de gradient

### 🎯 Objectif
Comprendre **comment un modèle apprend**. C'est LE chapitre central de toute l'IA moderne.

### 💡 L'essentiel en 5 minutes

Imagine que tu es sur une colline dans le brouillard et que tu veux descendre dans la vallée. Tu ne vois rien à plus de 2 mètres. Ta stratégie : **sentir la pente sous tes pieds, faire un petit pas dans la direction qui descend le plus, recommencer.**

- La **hauteur** = l'erreur du modèle (la *loss*, ou fonction de coût).
- **Sentir la pente** = calculer la **dérivée** (gradient).
- **Le petit pas** = le **learning rate** (α, taux d'apprentissage).
- **Descendre** = mettre à jour les poids : $w \leftarrow w - \alpha \cdot \frac{\partial L}{\partial w}$.

C'est tout. Toute l'IA moderne fonctionne avec cette boucle. GPT, Stable Diffusion, AlphaGo : même principe.

### 📘 Le cours

#### 5.1 Dérivée = vitesse de variation
La dérivée $f'(x)$ mesure **de combien change $f$ quand $x$ change un tout petit peu**.
- $f(x) = x^2 \Rightarrow f'(x) = 2x$. En $x=3$, la pente vaut 6.
- $f(x) = 3x + 1 \Rightarrow f'(x) = 3$ (pente constante : c'est une droite).

| Fonction $f(x)$ | Dérivée $f'(x)$ | Utilité en IA |
|---|---|---|
| $x^n$ | $n x^{n-1}$ | fonctions de coût |
| $e^x$ | $e^x$ | sigmoïde, softmax |
| $\ln(x)$ | $1/x$ | log-loss, entropie croisée |
| $\sigma(x)=\frac{1}{1+e^{-x}}$ | $\sigma(x)(1-\sigma(x))$ | neurone binaire |

**Règles à connaître :**
- $(f+g)' = f' + g'$
- $(f \times g)' = f'g + fg'$ (produit)
- **Dérivée composée (chain rule)** : $\big(f(g(x))\big)' = f'(g(x)) \cdot g'(x)$ ← **c'est cette règle qui est au cœur de la rétropropagation (backpropagation) des réseaux de neurones.**

#### 5.2 Dérivée partielle et gradient
Quand une fonction dépend de plusieurs variables (plein de poids !), on dérive par rapport à **une** variable en gardant les autres fixes : c'est une **dérivée partielle**, notée $\partial$.
Le **gradient** $\nabla L$ est le vecteur de toutes les dérivées partielles : il pointe vers la **direction de plus forte augmentation**. Donc pour minimiser, on va dans la direction **opposée** : $-\nabla L$.

#### 5.3 La descente de gradient, pas à pas

1. Initialiser les poids au hasard.
2. Prédire : $\hat{y} = Xw + b$.
3. Calculer l'erreur : par exemple l'erreur quadratique moyenne $L = \frac{1}{n}\sum_i (\hat{y}_i - y_i)^2$.
4. Calculer le gradient de L par rapport à w et b.
5. Mettre à jour : $w \leftarrow w - \alpha \frac{\partial L}{\partial w}$, $b \leftarrow b - \alpha \frac{\partial L}{\partial b}$.
6. Répéter (des centaines/millions de fois, en avançant par « mini-lots » = *batch*).

**Pour la régression linéaire, les gradients se calculent très simplement :**
$$\frac{\partial L}{\partial w} = \frac{2}{n} X^T (\hat{y} - y) \qquad \frac{\partial L}{\partial b} = \frac{2}{n}\sum_i (\hat{y}_i - y_i)$$

#### 5.4 Le learning rate (α) : le réglage le plus important
| α | Conséquence |
|---|---|
| Trop petit (ex. 0,0000001) | apprentissage interminable, tu abandonnes avant la vallée |
| Bien choisi (0,001 → 0,1) | descente douce et régulière |
| Trop grand (ex. 10) | ça oscille, ça diverge, la loss explose (NaN) |

**Astuce pratique :** si la loss affiche `nan` ou explose → **réduis α de 10×**. Si la loss descend trop lentement → augmente α de 3×.

#### 5.5 Le piège du minimum local (et la solution : le SGD)
La descente « complète » (full-batch) suit la vraie pente mais est lente sur gros volumes. Le **SGD (Stochastic Gradient Descent)** utilise un petit lot aléatoire (ex. 32 exemples) : c'est bruité, plus rapide, et le bruit aide à sortir des mauvais minimums. Variantes à connaître par leur nom : **Momentum, RMSProp, Adam / AdamW** (Adam = le standard par défaut en deep learning).

#### 5.6 Les 3 fonctions de coût à connaître
| Tâche | Loss | Formule simplifiée |
|---|---|---|
| Régression (prédire un nombre) | MSE | $\frac{1}{n}\sum(\hat y - y)^2$ |
| Classification binaire | Log-loss / entropie croisée | $-\frac{1}{n}\sum[\,y\log\hat y + (1-y)\log(1-\hat y)\,]$ |
| Classification multiple | Entropie croisée catégorielle | $-\frac{1}{n}\sum_c y_c \log \hat y_c$ |

### ⚠️ Les 3 erreurs classiques
1. **Ne pas normaliser les entrées** → gradients déséquilibrés, ça diverge. Normalise toujours (chapitre 2.6).
2. **Regarder la loss sans regarder les 2 courbes (train et validation)** → tu ne verras pas l'overfitting (chapitre suivant).
3. **Changer 5 réglages à la fois** → tu ne sauras jamais ce qui a marché. **Une variable à la fois.**

### 💻 Code du chapitre (à taper et exécuter : tu écris ton premier apprentissage !)
```python
import numpy as np

# 1. Données synthétiques : y = 3x + 2 + bruit
rng = np.random.default_rng(0)
X = rng.uniform(0, 10, size=(200, 1))
y = 3 * X[:, 0] + 2 + rng.normal(0, 1, size=200)

# 2. Normalisation (moyenne 0, écart-type 1)
Xm, Xs = X.mean(axis=0), X.std(axis=0)
Xn = (X - Xm) / Xs

# 3. Descente de gradient
w = np.zeros(1)
b = 0.0
alpha = 0.1
n = len(y)

for epoch in range(1000):
    yhat = Xn @ w + b
    loss = ((yhat - y) ** 2).mean()
    dw = 2 / n * Xn.T @ (yhat - y)
    db = 2 / n * (yhat - y).sum()
    w -= alpha * dw
    b -= alpha * db
    if epoch % 200 == 0:
        print(f"epoch {epoch:4d} | loss = {loss:.3f}")

print("Poids normalisé :", w, "| biais :", b)
# Repasser en unités d'origine : pente = w/Xs, ordonnée = b - w*Xm/Xs
print("Droite apprise : pente ≈", (w / Xs)[0], "| ordonnée ≈", (b - w * Xm / Xs)[0], "| vraie pente : 3")
```

### ✅ Quiz
1. Que représente la dérivée d'une fonction ?
2. Dans quelle direction va-t-on pour minimiser une fonction : $+\nabla L$ ou $-\nabla L$ ?
3. Que se passe-t-il si α est trop grand ?
4. Quelle règle de dérivation rend la backpropagation possible ?
5. Pourquoi le SGD est-il préféré au full-batch sur de gros jeux de données ?

### 🛠️ Exercices
1. Reprends le code et lance-le avec `alpha = 0.001`, `0.1`, `1.0`, `5.0`. Note la loss finale dans un tableau. Que observes-tu ?
2. Ajoute un second poids : génère `y = 3*x1 - 2*x2 + 5 + bruit` et fais apprendre `w = [w1, w2]` (matrice `X` de shape (n,2)). Retrouve les vrais coefficients.
3. Remplace l'erreur quadratique par l'erreur absolue `|yhat - y|` : le gradient devient le **signe** de l'erreur. Est-ce que ça converge ?
4. **Projet fil rouge** : applique cette descente de gradient à une vraie variable de ton dataset (ex. prédire le prix à partir du poids). Trace la droite apprise avec matplotlib.

---

# CHAPITRE 6 — Maths 3 : probabilités et statistiques

### 🎯 Objectif
Savoir décrire de l'incertitude, comprendre un test statistique, et savoir **évaluer honnêtement** un modèle (moyenne ≠ vérité, corrélation ≠ causalité).

### 💡 L'essentiel en 5 minutes

Un modèle d'IA ne dit jamais « c'est ça », il dit **« j'estime à 82 % de chances que ce soit ça »**. Pour comprendre ça, il faut parler probabilités : événements, probabilité conditionnelle, distributions, et échantillonnage.

### 📘 Le cours

#### 6.1 Probabilité : les bases
- $P(A) \in [0, 1]$. `P(pluie demain) = 0,3`.
- **Complémentaire** : $P(\text{pas } A) = 1 - P(A)$.
- **Union (A ou B)** : $P(A\cup B) = P(A) + P(B) - P(A\cap B)$.
- **Intersection (A et B)** : si indépendants, $P(A\cap B) = P(A)P(B)$.

#### 6.2 Probabilité conditionnelle et théorème de Bayes (crucial)
$P(A\mid B) = \dfrac{P(A\cap B)}{P(B)}$ — « probabilité de A sachant que B est arrivé ».

**Bayes** : $P(A\mid B) = \dfrac{P(B\mid A)\,P(A)}{P(B)}$

Vocabulaire : **prior** (croyance avant), **vraisemblance** (les données), **posterior** (croyance après).

**Exemple santé (important en IA appliquée) :** une maladie touche 1 % de la population. Le test est positif à 99 % chez les malades et à 5 % chez les sains. Résultat positif → quelle probabilité d'être malade ?
- Prior : 0,01.
- Sur 10 000 personnes : 100 malades → 99 positifs ; 9 900 sains → 495 faux positifs.
- Donc $P(\text{malade} \mid +) = 99 / (99+495) \approx 16{,}7\%$.

**Leçon généralisable : quand la classe est rare, un modèle avec 99 % d'exactitude peut être mauvais.** C'est le piège n°1 des débutants en classification.

#### 6.3 Statistiques descriptives (ce qu'on lit dans `df.describe()`)
| Mesure | Ce qu'elle dit | Piège |
|---|---|---|
| Moyenne | centre | très sensible aux extrêmes |
| Médiane | valeur du milieu | robuste (recommandée si outliers) |
| Écart-type | dispersion autour de la moyenne | $\sigma = \sqrt{\frac{1}{n}\sum(x_i-\bar x)^2}$ |
| Quantiles (Q1, médiane, Q3) | répartition | base des boîtes à moustaches |
| Corrélation (Pearson) | relation linéaire, de -1 à 1 | **corrélation ≠ causalité** |

**Détecter la « non-représentativité » :** vérifie toujours que tes données d'évaluation ressemblent à la réalité (même distribution d'âge, de ville, de période). Sinon ton 95 % d'exactitude ne veut rien dire dans le monde réel.

#### 6.4 Les distributions à connaître (par nom)
- **Uniforme** : toutes les valeurs équiprobables.
- **Normale (gaussienne)** : en cloche, paramétrée par μ (moyenne) et σ (écart-type). ~68 % des valeurs dans $[\mu-\sigma, \mu+\sigma]$, ~95 % dans $[\mu-2\sigma, \mu+2\sigma]$.
- **Bernoulli** : oui/non (pile ou face, spam ou pas).
- **Binomiale** : nombre de succès sur n essais.
- **Poisson** : nombre d'événements dans un intervalle (appels/heure).

#### 6.5 Échantillonnage, biais, variance
- **Biais** : ton estimation est *systématiquement* à côté (ex. : interroger uniquement « tout Ouagadougou » pour estimer le Burkina).
- **Variance** : tes estimations changent trop d'un échantillon à l'autre.
- **Biais-variance** = LE concept central du ML : un modèle trop simple → biais élevé (*underfitting*) ; trop complexe → variance élevée (*overfitting*). Voir la Partie 2.

#### 6.6 Tests d'hypothèses (culture utile)
- $H_0$ : « rien ne se passe » (hypothèse nulle) ; $H_1$ : « il y a un effet ».
- **p-value** : probabilité d'observer un effet au moins aussi fort *si $H_0$ est vraie*. Si p < 0,05, on rejette $H_0$ (seuil conventionnel, pas une vérité absolue).
- **Intervalle de confiance à 95 %** : plage qui contiendrait la vraie valeur dans 95 % des tirages.
- **A/B testing** : version A vs version B, avec test statistique → c'est ainsi que les entreprises mesurent l'impact d'un modèle en production.

### ⚠️ Les 3 erreurs classiques
1. **Optimiser l'exactitude sur des classes déséquilibrées.** Sur 99 % de « non-malades », un modèle qui répond toujours « sain » a 99 % d'exactitude… et 0 utilité.
2. **Confondre corrélation et causalité** (les ventes de glaces et les noyades augmentent ensemble : la cause est l'été).
3. **Utiliser la moyenne sur des données asymétriques** (revenus, prix) → préfère la médiane.

### 💻 Code du chapitre
```python
import numpy as np

rng = np.random.default_rng(1)

# Simulation du test médical du cours
n = 100_000
malade = rng.random(n) < 0.01                       # 1 % de malades
test_positif = np.where(malade, rng.random(n) < 0.99, rng.random(n) < 0.05)

p_malade_si_positif = malade[test_positif].mean()
print(f"P(malade | test positif) = {p_malade_si_positif:.3f}")   # ≈ 0,16

# Asymétrie : moyenne vs médiane
revenus = rng.lognormal(mean=10, sigma=1, size=10_000)
print("moyenne :", round(revenus.mean()), "| médiane :", round(np.median(revenus)))
```

### ✅ Quiz
1. Si $P(A)=0,3$ et $P(B)=0,4$ et A,B indépendants, $P(A\cap B)$ ?
2. Écris la formule de Bayes de mémoire.
3. Un modèle détecte 95 % des cancers mais produit beaucoup de faux positifs. Vaut-il mieux qu'un modèle qui en détecte 80 % sans faux positifs ? (Discute : en dépistage médical, on privilégie souvent la sensibilité.)
4. Que mesure l'écart-type ?
5. Pourquoi la médiane est-elle plus robuste que la moyenne ?

### 🛠️ Exercices
1. Simule 1 000 lancers d'un dé truqué (probabilité du 6 : 0,3) et estime la probabilité de chaque face. Précision → compare avec 10 000 lancers.
2. Calcule à la main (puis en Python) la probabilité qu'un patient soit malade sachant deux tests positifs successifs, avec les chiffres du cours.
3. Calcule la corrélation entre deux colonnes de ton dataset et écris en une phrase pourquoi ce n'est pas une causalité.
4. **Projet fil rouge** : décris en 5 lignes la distribution de ta variable cible (moyenne, médiane, min, max, % de valeurs manquantes) et propose une stratégie d'imputation.

---

## 🏁 Fin de la Partie 1 : auto-évaluation

Tu es prêt pour la Partie 2 si tu peux, **sans regarder** :
- [ ] écrire une fonction Python avec boucle, condition et gestion d'erreur ;
- [ ] créer un tableau NumPy, le normaliser, et faire un `X @ w` ;
- [ ] charger un CSV avec Pandas, compter les valeurs manquantes, faire un `groupby` ;
- [ ] expliquer avec tes mots : produit scalaire, gradient, descente de gradient, learning rate ;
- [ ] expliquer pourquoi l'exactitude seule est trompeuse ;
- [ ] montrer ton dépôt GitHub avec 3 notebooks et un README.

Si oui → **Partie 2**. Si non → refais les exercices concernés (1 semaine max), puis avance. Ne reste pas bloqué : avancer avec 85 % de maîtrise est la bonne stratégie.

# PARTIE 3 — DEEP LEARNING : les réseaux de neurones

> **Durée prévue :** semaines 27 à 39 (5-10 h/semaine)
> **Objectif de fin de partie :** comprendre et entraîner un réseau de neurones, utiliser des modèles pré-entraînés (transfer learning), et savoir *quand* le deep learning est pertinent (souvent moins souvent qu'on ne le croit).
>
> ⚠️ **Vérité utile :** sur des **données tabulaires**, le deep learning perd souvent contre LightGBM (chapitre 11). Le DL gagne sur les **images, le texte, l'audio, la vidéo** et les **très gros volumes**. Savoir dire ça en entretien vaut de l'or.

| Chapitre | Sujet | Semaines |
|---|---|---|
| 14 | Du neurone au réseau | 27-29 |
| 15 | Entraîner un réseau (PyTorch pratique) | 29-31 |
| 16 | Vision : les CNN | 31-34 |
| 17 | Séquences : RNN, LSTM, séries temporelles | 34-36 |
| 18 | Attention et Transformers | 36-38 |
| 19 | Transfer learning et Hugging Face | 38-39 |

**Outils à installer (Colab les a déjà) :** `torch torchvision transformers datasets` — sur ta machine : `pip install torch torchvision`.

---

# CHAPITRE 14 — Du neurone au réseau

### 🎯 Objectif
Comprendre ce qu'est un neurone artificiel, une couche, une fonction d'activation, et pourquoi un réseau peut apprendre des choses non linéaires.

### 💡 L'essentiel en 5 minutes

**Un neurone artificiel = une mini-décision.**
Il fait 3 choses : (1) il **pèse** ses entrées, (2) il les **additionne** avec un biais, (3) il **décide** via une fonction d'activation.

$$\text{sortie} = f(w_1x_1 + w_2x_2 + \dots + b)$$

Un neurone seul, c'est une droite. **Empilé en couches**, ça devient capable de dessiner n'importe quelle frontière, même très courbe. C'est ça, le « deep » dans deep learning : **plusieurs couches**.

### 📘 Le cours

#### 14.1 Le perceptron et sa limite
Le perceptron (1958) : `sortie = 1 si w·x + b > 0, sinon 0`.
**Limite historique** : il ne peut pas apprendre le XOR (ou exclusif) — un problème non linéairement séparable. Cette limite a gelé la recherche pendant des années… jusqu'aux couches cachées.

**Leçon :** sans non-linéarité, empiler des couches = une seule couche. Les **fonctions d'activation** sont donc essentielles, pas décoratives.

#### 14.2 Les fonctions d'activation (à connaître par cœur)
| Nom | Formule | Usage | Remarque |
|---|---|---|---|
| **ReLU** | $\max(0, x)$ | standard des couches cachées | rapide, mais « neurones morts » possibles |
| **Leaky ReLU / GELU** | variantes | moderne (GELU dans les Transformers) | corrige les neurones morts |
| **Sigmoïde** | $\frac{1}{1+e^{-x}}$ | sortie binaire | sature → gradients qui disparaissent |
| **Tanh** | $\frac{e^x-e^{-x}}{e^x+e^{-x}}$ | centré en 0 | même problème de saturation |
| **Softmax** | $\frac{e^{z_i}}{\sum_j e^{z_j}}$ | sortie multiclasse | sort une distribution qui somme à 1 |

**Règle pratique :** ReLU/GELU au milieu, sigmoïde pour 1 seule sortie binaire, softmax pour N classes.

#### 14.3 Architecture d'un réseau dense (MLP)
```
entrée (30 variables)
   ↓ couche cachée 1 : 128 neurones + ReLU
   ↓ couche cachée 2 : 64 neurones + ReLU
   ↓ couche de sortie : 1 neurone + Sigmoïde
```
Un **MLP** (Multi-Layer Perceptron) = couches entièrement connectées.
**Compter les paramètres :** entre une couche de 30 entrées et 128 neurones : $30 \times 128$ poids $+ 128$ biais $= 3968$ paramètres. Un modèle de vision a des millions, GPT en a des centaines de milliards.

#### 14.4 Le théorème d'approximation universelle (à savoir citer)
Un réseau avec **une seule couche cachée suffisamment large** peut approximer n'importe quelle fonction continue. En pratique, on empile plusieurs couches plus petites : c'est plus efficace en paramètres, ça hiérarchise l'information (bords → formes → objets).

#### 14.5 Vocabulaire à maîtriser
- **Époque (epoch)** : un passage complet sur les données d'entraînement.
- **Batch / mini-batch** : sous-ensemble (ex. 32 exemples) utilisé pour un pas de gradient.
- **Itération** : un pas d'optimisation (1 batch).
- **Learning rate** : taille du pas.
- **Dropout** : on éteint aléatoirement des neurones pendant l'entraînement (régularisation).
- **BatchNorm / LayerNorm** : normalisent les activations → entraînement plus stable et plus rapide.
- **Early stopping** : on garde le meilleur modèle sur la validation.

### ⚠️ Les 3 erreurs classiques
1. **Oublier la non-linéarité** → le réseau reste un modèle linéaire, peu importe le nombre de couches.
2. **Mettre softmax + entropie croisée « binaire »** → incohérence de loss. (En PyTorch, `CrossEntropyLoss` **inclut** déjà le softmax : n'ajoutez pas de softmax avant !)
3. **Trop gros réseau dès le départ** sur un petit dataset → overfitting immédiat.

### ✅ Quiz
1. Écris la formule d'un neurone.
2. Pourquoi le perceptron simple n'apprend-il pas XOR ?
3. ReLU pour les couches cachées, softmax pour la sortie : pourquoi ce partage ?
4. Différence entre époque, batch et itération ?
5. Que fait le dropout ?

### 🛠️ Exercice
Sur papier (ou dans un notebook) : dessine un réseau `3 → 4 → 2`. Écris les matrices de poids et vérifie les dimensions comme au chapitre 4 (produit matriciel). Combien de paramètres au total ?

---

# CHAPITRE 15 — Entraîner un réseau : PyTorch pas à pas

### 🎯 Objectif
Écrire une boucle d'entraînement complète de A à Z, et diagnostiquer les problèmes (loss qui bouge pas, overfitting, NaN).

### 💡 L'essentiel en 5 minutes

La boucle d'entraînement, c'est **5 lignes** :
```
pour chaque batch :
   1. prédire           ← forward
   2. calculer l'erreur ← loss
   3. vider les gradients ← zero_grad
   4. calculer les gradients ← backward
   5. mettre à jour les poids ← optimizer.step
```
Tout le deep learning, sans exception, tourne autour de ces 5 lignes.

### 📘 Le cours

#### 15.1 Le code complet, commenté ligne par ligne
```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
import numpy as np

# --- Données (problème non linéaire, impossible pour un modèle linéaire) ---
X, y = make_moons(n_samples=2000, noise=0.25, random_state=0)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=0, stratify=y)

X_tr = torch.tensor(X_tr, dtype=torch.float32)
y_tr = torch.tensor(y_tr, dtype=torch.float32).view(-1, 1)
X_te = torch.tensor(X_te, dtype=torch.float32)
y_te = torch.tensor(y_te, dtype=torch.float32).view(-1, 1)

loader = DataLoader(TensorDataset(X_tr, y_tr), batch_size=64, shuffle=True)

# --- Modèle ---
class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(2, 32), nn.ReLU(),
            nn.Linear(32, 32), nn.ReLU(),
            nn.Linear(32, 1), nn.Sigmoid(),      # sortie entre 0 et 1
        )
    def forward(self, x):
        return self.net(x)

modele = MLP()
loss_fn = nn.BCELoss()                                # binaire
optimizer = torch.optim.Adam(modele.parameters(), lr=1e-3)

# --- Boucle d'entraînement ---
for epoch in range(50):
    modele.train()                                     # mode entraînement (dropout/BN actifs)
    pertes = []
    for xb, yb in loader:
        pred = modele(xb)                              # 1. forward
        loss = loss_fn(pred, yb)                       # 2. erreur
        optimizer.zero_grad()                          # 3. vider les gradients accumulés
        loss.backward()                                # 4. rétropropagation
        optimizer.step()                               # 5. mise à jour des poids
        pertes.append(loss.item())

    # --- Évaluation ---
    modele.eval()                                      # mode évaluation (dropout désactivé)
    with torch.no_grad():                              # pas de gradients → plus rapide
        pred_te = modele(X_te)
        acc = ((pred_te > 0.5).float() == y_te).float().mean().item()
    if epoch % 10 == 0:
        print(f"epoch {epoch:2d} | loss = {np.mean(pertes):.4f} | accuracy test = {acc:.3f}")
```

#### 15.2 La rétropropagation (backpropagation) expliquée simplement
C'est la **règle de la chaîne** appliquée dans le sens inverse :
1. **Forward** : on calcule la prédiction couche par couche, en gardant les valeurs intermédiaires.
2. **Loss** : on mesure l'erreur finale.
3. **Backward** : on remonte la chaîne pour obtenir la dérivée de la loss par rapport à **chaque** poids (∂L/∂w). Chaque couche multiplie sa dérivée locale par celle venant du dessus.
4. **Update** : on applique la descente de gradient.

Analogie : dans une chaîne de production qui rate un produit final, on remonte la chaîne pour savoir **quel poste** est responsable et de combien il faut ajuster.

#### 15.3 Comment le réseau « apprend » concrètement
Les poids commencent aléatoires → prédictions mauvaises → les gradients indiquent dans quel sens corriger **chaque** poids → petit pas → on répète. Après des milliers d'itérations, les poids encodent des régularités utiles.

#### 15.4 Diagnostic : que faire quand ça ne marche pas ?
| Symptôme | Cause probable | Action |
|---|---|---|
| Loss constante, ne bouge pas | learning rate trop petit, mauvais loss_fn, données non normalisées | monte lr ×10, vérifie les formes, normalise |
| Loss = NaN | lr trop grand, log(0) dans la loss | baisse lr ×10, gradient clipping, `+1e-7` |
| Train 99 %, test 70 % | **overfitting** | dropout, augmentation de données, weight decay, early stopping, plus de données |
| Train 60 %, test 60 % | **underfitting** | réseau plus gros, plus d'epochs, meilleures features |
| Loss baisse puis remonte | overfitting en cours | **early stopping** (garder le meilleur epoch) |
| Résultats qui changent à chaque run | graines non fixées | `torch.manual_seed(42)`, `np.random.seed(42)` |

#### 15.5 Les leviers de régularisation (à connaître)
```python
nn.Dropout(0.3)                                     # couche de dropout
optimizer = torch.optim.AdamW(modele.parameters(), lr=1e-3, weight_decay=1e-4)  # L2
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=50)     # lr qui décroît
```
- **Augmentation de données** (images : rotations, flips — voir chapitre 16) : le levier le plus puissant en vision.
- **Early stopping** : arrêter à l'epoch où la validation est la meilleure.
- **Transfer learning** : réutiliser un modèle pré-entraîné (chapitre 19) — la **vraie** solution quand tu as peu de données.

#### 15.6 Bonnes pratiques professionnelles
- **Normalise** tes entrées (moyenne 0, écart-type 1).
- **Fixe les graines** : résultats reproductibles = crédibilité.
- **Sépare entraînement/validation/test** dès le début ; la validation pilote l'early stopping, le test juge à la fin.
- **Sauvegarde le meilleur modèle** :
```python
torch.save(modele.state_dict(), "models/mlp.pt")
modele.load_state_dict(torch.load("models/mlp.pt"))
```
- **Journalise** tes essais (lr, taille du réseau, score) dans un petit CSV — ton futur toi te remerciera.

### 💻 Code du chapitre
Utilise et **modifie** le code de la section 15.1 : passe à 3 couches, ajoute du dropout 0,3, un weight_decay, puis compare les scores. Note tout dans `reports/experiences.csv`.

### ⚠️ Les 3 erreurs classiques
1. **Oublier `optimizer.zero_grad()`** → les gradients s'accumulent, l'entraînement diverge.
2. **Oublier `modele.eval()` + `torch.no_grad()`** en évaluation → dropout actif, résultats faux et lents.
3. **Mettre `nn.Softmax()` avant `nn.CrossEntropyLoss()`** → double application, loss fausse.

### ✅ Quiz
1. Cite les 5 étapes d'une boucle d'entraînement.
2. Que fait `loss.backward()` ?
3. Pourquoi `zero_grad()` avant `backward()` ?
4. Ton train est à 99 % et ton test à 68 % : 4 solutions ?
5. Pourquoi ne pas utiliser softmax avec CrossEntropyLoss en PyTorch ?

### 🛠️ Exercice
Reprends **ton dataset tabulaire** du projet fil rouge : entraîne un MLP et compare-le à LightGBM (AUC ou accuracy). Qui gagne ? Écris 5 lignes d'explication — c'est exactement la question posée en entretien junior.

---

# CHAPITRE 16 — Vision : les réseaux convolutifs (CNN)

### 🎯 Objectif
Comprendre pourquoi les CNN écrasent le MLP en images, et savoir entraîner un classifieur d'images (dont le tien, sur un problème africain réel).

### 💡 L'essentiel en 5 minutes

Un MLP sur une image 224×224×3 = 150 528 entrées. Il apprendrait « le pixel (12, 87) est important », ce qui ne veut rien dire : si l'objet se décale de 10 pixels, tout change.

**Le CNN** balade un petit **filtre** (3×3 par ex.) sur l'image et détecte un motif **partout** :
- Couche 1 : détecte des **bords** et des couleurs.
- Couche 2 : détecte des **formes** (coins, textures).
- Couche 3 : détecte des **objets** (œil, roue).
- Couche finale : dit **« c'est un chien »**.

Trois idées clés : **convolutions** (détecter un motif partout), **pooling** (résumer/réduire), **poids partagés** (le même filtre partout → très peu de paramètres).

### 📘 Le cours

#### 16.1 La convolution, concrètement
Un filtre 3×3 :
```
-1  0  1
-1  0  1
-1  0  1
```
Ce filtre réagit aux **bords verticaux**. Il glisse sur l'image : à chaque position, il multiplie les 9 pixels par les 9 poids et somme → une carte d'activation qui vaut fort là où il y a un bord vertical.

Un CNN apprend **des milliers** de filtres ; il découvre lui-même lesquels sont utiles.

**Hyperparamètres :**
- `kernel_size` (3, 5…) : taille du filtre.
- `stride` : pas de déplacement (1 = image même taille, 2 = divisée par 2).
- `padding` : bords remplis de 0 pour contrôler la taille de sortie.
- `channels` (filtres) : nombre de motifs détectés (32, 64, 128…).

**Formule magique :** $\text{sortie} = \frac{\text{entrée} - k + 2p}{s} + 1$ (utile pour vérifier tes `shape`).

#### 16.2 Pooling
`MaxPool2d(2)` prend le maximum de chaque carré 2×2 → l'image est divisée par 2 en largeur et hauteur. Effet : résistance aux petits décalages + moins de calcul.

#### 16.3 Architecture typique
```
Entrée 3×32×32
 → [Conv 3→32, k=3, pad=1] → ReLU → MaxPool2 → 32×16×16
 → [Conv 32→64, k=3, pad=1] → ReLU → MaxPool2 → 64×8×8
 → Flatten (64×8×8 = 4096)
 → Linear 4096→128 → ReLU → Dropout(0.3)
 → Linear 128→10  (10 classes)
```

#### 16.4 Code complet (CIFAR-10, explicable en entretien)
```python
import torch, torch.nn as nn, torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

device = "cuda" if torch.cuda.is_available() else "cpu"
print("Appareil :", device)

tf = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
    transforms.RandomHorizontalFlip(),        # ← augmentation de données
    transforms.RandomCrop(32, padding=4),
])
train_ds = datasets.CIFAR10(root="./data", train=True, download=True, transform=tf)
test_ds  = datasets.CIFAR10(root="./data", train=False, download=True,
                            transform=transforms.Compose([transforms.ToTensor(),
                            transforms.Normalize((0.5,)*3, (0.5,)*3)]))

train_ld = DataLoader(train_ds, batch_size=128, shuffle=True, num_workers=2)
test_ld  = DataLoader(test_ds, batch_size=256)

class CNN(nn.Module):
    def __init__(self, n_classes=10):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),   # 32→16
            nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),  # 16→8
            nn.Conv2d(64, 128, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2), # 8→4
        )
        self.classifier = nn.Sequential(
            nn.Flatten(), nn.Linear(128*4*4, 256), nn.ReLU(), nn.Dropout(0.3),
            nn.Linear(256, n_classes),
        )
    def forward(self, x):
        return self.classifier(self.features(x))

modele = CNN().to(device)
loss_fn = nn.CrossEntropyLoss()                # inclut le softmax
opt = torch.optim.AdamW(modele.parameters(), lr=1e-3, weight_decay=1e-4)
sched = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=3e-3, total_steps=15*len(train_ld))

for epoch in range(15):
    modele.train()
    for xb, yb in train_ld:
        xb, yb = xb.to(device), yb.to(device)
        pred = modele(xb)
        loss = loss_fn(pred, yb)
        opt.zero_grad(); loss.backward(); opt.step(); sched.step()

    modele.eval(); bon = total = 0
    with torch.no_grad():
        for xb, yb in test_ld:
            xb, yb = xb.to(device), yb.to(device)
            pred = modele(xb).argmax(1)
            bon += (pred == yb).sum().item(); total += yb.size(0)
    print(f"epoch {epoch+1:2d} | accuracy test = {bon/total:.3f}")
```
**Résultat attendu : ~75-85 %** sur CIFAR-10 après 15 epochs. C'est un excellent exercice de portfolio : « chat vs chien », « cultures », « maladies de plantes ».

#### 16.5 Transfer learning en vision (à utiliser dès que tu as peu de données)
```python
from torchvision import models
import torch.nn as nn

resnet = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
for p in resnet.parameters():          # 1. geler le modèle pré-entraîné
    p.requires_grad = False
resnet.fc = nn.Linear(resnet.fc.in_features, 5)   # 2. nouvelle tête pour 5 classes
# 3. entraîner seulement la tête (rapide), puis éventuellement dégeler les dernières couches
```
**Avec 300 images par classe**, un ResNet18 pré-entraîné **bat** un CNN entraîné de zéro. C'est LA technique clé en pratique.

#### 16.6 Applications réelles inspirantes (et africaines)
- Détection de **maladies des cultures** (maïs, mil, tomate) à partir de photos prises au téléphone — datasets publics existants (PlantVillage).
- Comptage de **plants** ou de **bétail** par drone.
- Lecture automatique de **compteurs** d'eau/électricité.
- Détection de **masques**/EPI sur chaîne de production (sécurité).
- Imagerie médicale (paludisme : classification de frottis sanguins, radiographies).

### ⚠️ Les 3 erreurs classiques
1. **Mettre un Flatten avant un MaxPool** ou se tromper dans l'ordre → erreur de dimension. **Calcule tes `shape` à la main**, c'est l'exercice n°1.
2. **Mélanger les images du même patient/plant entre train et test** → fuite massive, score illusoire.
3. **Utiliser des images non normalisées** et des couleurs différentes entre train et test (grand angle, éclairage) → chute de performance en production. **La robustesse des données prime sur l'architecture.**

### ✅ Quiz
1. Pourquoi un CNN a-t-il beaucoup moins de paramètres qu'un MLP équivalent ?
2. Que fait un filtre de convolution ?
3. À quoi sert le max-pooling ?
4. Sortie d'une conv 1 canal, kernel 5, padding 0, stride 1, sur une entrée 28×28 ?
5. Avec 200 photos par classe, quelle stratégie choisis-tu en premier ?

### 🛠️ Exercices
1. Entraîne le CNN du chapitre sur **Fashion-MNIST** (plus visuel que MNIST) et atteins ≥ 90 % d'accuracy.
2. Prends un dataset public de **maladies de plantes** (Kaggle : *PlantVillage*), fais un transfer learning ResNet18, atteins ≥ 92 % sur 5 classes.
3. **Essai d'ablation** : entraîne ton modèle (a) sans augmentation, (b) sans dropout, (c) sans les deux. Tableau comparatif + conclusion. C'est ce type de démarche qui impressionne en entretien.

---

# CHAPITRE 17 — Séquences : RNN, LSTM et séries temporelles

### 🎯 Objectif
Savoir traiter des données **ordonnées dans le temps** : texte, audio, mesures, ventes, météo.

### 💡 L'essentiel en 5 minutes

Un RNN lit la séquence **un élément à la fois** et garde une **mémoire** (état caché) : « je me souviens de ce que j'ai lu avant ». Problème : il **oublie** sur de longues séquences (gradients qui disparaissent). Le **LSTM** (et le GRU) résout ça avec des **portes** : « qu'est-ce que je garde, qu'est-ce que j'oublie, qu'est-ce que je sors ».

Aujourd'hui, pour le texte, les Transformers (chapitre 18) ont remplacé les RNN. Mais les **LSTM/GRU restent excellents** sur les séries numériques (capteurs, énergie, prix) et les petites données.

### 📘 Le cours

#### 17.1 Formulations
- **RNN simple** : $h_t = \tanh(W_x x_t + W_h h_{t-1} + b)$ — l'état caché $h_t$ résume le passé.
- **LSTM** : ajoute une **cellule mémoire** $c_t$ et 3 portes (oubli, entrée, sortie) qui dosent l'information conservée.
- **GRU** : version allégée du LSTM (2 portes), souvent aussi efficace et plus rapide.
- **Bidirectionnel** : lit la séquence dans les deux sens (utile en NLP : le mot suivant éclaire le précédent).

#### 17.2 Code : classification de texte avec un GRU
```python
import torch, torch.nn as nn

class ClassifieurTexte(nn.Module):
    def __init__(self, vocab_size, dim_embed=64, cache=128, n_classes=2):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, dim_embed, padding_idx=0)
        self.gru = nn.GRU(dim_embed, cache, batch_first=True, bidirectional=True)
        self.fc = nn.Linear(cache*2, n_classes)
    def forward(self, x):                     # x : (batch, longueur) d'indices de mots
        e = self.embed(x)                     # (batch, longueur, dim)
        sorties, h = self.gru(e)              # h : état final
        h2 = torch.cat([h[0], h[1]], dim=-1)  # concatène les 2 sens
        return self.fc(h2)
```
🔑 **Embedding** : convertir un mot (ou un identifiant) en **vecteur dense** appris. Deux mots utilisés de la même façon finissent avec des vecteurs proches → la machine découvre la proximité de sens. C'est la brique de base du NLP, et des LLM.

#### 17.3 Séries temporelles : la méthode qui marche vraiment
Pour prédire des valeurs numériques (ventes, consommation, prix), combine :
1. **Variables de décalage (lags)** : `y[t-1]`, `y[t-2]`, `y[t-7]`, `y[t-30]` → très puissantes.
2. **Variables calendaires** : jour de la semaine, mois, jours fériés, saison (essentiel : la saisonnalité des pluies au Sahel !).
3. **Moyennes mobiles** : `moyenne(y, fenêtre=7)`, écarts à la moyenne.
4. **Modèles** : LightGBM sur les variables ci-dessus (souvent le meilleur et le plus simple), ou LSTM/GRU, ou méthodes classiques (**SARIMA**, **Prophet**) comme baseline.
5. **Validation temporelle obligatoire** : `TimeSeriesSplit`, jamais de `train_test_split(random)`.

```python
import pandas as pd
df = df.sort_values("date")
for lag in [1, 2, 7, 30]:
    df[f"lag_{lag}"] = df["valeur"].shift(lag)
df["moy_7"] = df["valeur"].rolling(7).mean()
df["jour_semaine"] = pd.to_datetime(df["date"]).dt.dayofweek
df = df.dropna()          # les lags créent des NaN au début
```
**Métriques** : MAE, RMSE, **MAPE** (erreur en %, très parlante en entreprise), et **MASE** (comparaison à un modèle naïf).

**Baselines à battre absolument :** « demain = aujourd'hui » (persistance) et « même jour la semaine dernière ». Beaucoup de modèles complexes perdent contre ces deux règles.

#### 17.4 LSTM sur une série (exemple condensé)
```python
class LSTMPrevision(nn.Module):
    def __init__(self, n_features, cache=64):
        super().__init__()
        self.lstm = nn.LSTM(n_features, cache, batch_first=True, num_layers=2, dropout=0.2)
        self.fc = nn.Linear(cache, 1)
    def forward(self, x):                     # x : (batch, fenêtre, features)
        out, _ = self.lstm(x)
        return self.fc(out[:, -1, :])         # prédiction à partir du dernier pas
```
Fenêtre typique : 30-90 pas en entrée → 1 valeur (ou 7 jours) en sortie.

### ⚠️ Les 3 erreurs classiques
1. **Mélanger les dates au hasard** dans le split → fuite temporelle (ton score sera faux en production).
2. **Oublier la saisonnalité** (semaine, mois, pluies) → le modèle « ne comprend rien » aux grandes variations.
3. **Utiliser un LSTM là où LightGBM sur lags suffit** → tu perds du temps, de la performance et de la maintenabilité.

### ✅ Quiz
1. Qu'est-ce qu'un état caché ?
2. Pourquoi un RNN oublie-t-il sur de longues séquences ?
3. Que fait un layer d'embedding ?
4. Comment valider une série temporelle ?
5. Cite 2 baselines à battre avant d'annoncer un modèle de prévision.

### 🛠️ Exercices
1. Prédiction de consommation : prends une série publique (énergie, météo, prix agricoles) et bats la baseline de persistance avec LightGBM + lags. Puis essaie un GRU et compare.
2. Classification de texte : entraîne le GRU du chapitre sur un dataset de SMS spam (ou d'avis clients en français) et atteins ≥ 95 % d'accuracy.
3. Calcule le MAPE et explique en une phrase à un responsable commercial ce que ça veut dire.

---

# CHAPITRE 18 — Attention et Transformers : l'architecture de GPT

### 🎯 Objectif
Comprendre l'architecture qui a tout changé. **C'est LA notion à maîtriser pour 2026** : tous les LLM en découlent.

### 💡 L'essentiel en 5 minutes

**Le problème de l'attention :** dans la phrase *« l'athlète a reçu son trophée parce qu'**il** avait gagné »*, que désigne « il » ? Le RNN doit mémoriser sur 8 mots. L'attention, elle, **regarde toute la phrase d'un coup** et pondère : « athlète » 0,7, « trophée » 0,2, « gagné » 0,1.

$$\text{Attention}(Q,K,V) = \text{softmax}\!\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

Traduction en français :
- **Q (Query)** : « ce que je cherche ».
- **K (Key)** : « ce que chaque mot propose comme étiquette ».
- **V (Value)** : « l'information que chaque mot transmet ».
- $QK^T$ : similarité entre ma question et chaque étiquette → un score par mot.
- $/\sqrt{d_k}$ : stabilisation (évite que les scores explosent).
- **softmax** : convertit les scores en poids qui somment à 1.
- **× V** : on fait la moyenne pondérée des informations → **la représentation enrichie par le contexte**.

**Multi-Head** : on fait ça plusieurs fois en parallèle (8 têtes) — l'une s'intéresse à la syntaxe, l'autre au sens, etc. puis on concatène.
**Empilement** : GPT-3 = 96 blocs de ce type. Chaque bloc = attention + réseau dense + normalisations.

### 📘 Le cours

#### 18.1 Le bloc Transformer
```
Entrée (vecteurs des mots + position)
   ↓
[Multi-Head Self-Attention]   ← chaque mot regarde tous les autres
   ↓ Add & LayerNorm (connexion résiduelle)
[Feed-Forward (dense x2)]     ← transformation non linéaire, « réflexion »
   ↓ Add & LayerNorm
→ sortie, à répéter N fois
```
**Pourquoi c'est parallélisable ?** Contrairement au RNN (séquentiel), l'attention traite tous les mots **en même temps** → utilisation massive de GPU. C'est la clé technique du boom des LLM.

**Encodeur / Décodeur :**
- **BERT** = encodeur (comprend, bon pour la classification et la recherche).
- **GPT / Llama / Mistral** = décodeur (génère du texte).
- **T5 / BART** = encodeur-décodeur (traduction, résumé).

#### 18.2 L'attention causale et l'apprentissage de GPT
GPT est entraîné avec une **attention masquée** : chaque mot ne peut regarder que les mots précédents (sinon il « verrait » la réponse). Objectif d'entraînement : **prédire le mot suivant** sur des milliards de textes. C'est tout. C'est incroyablement simple… et c'est ce qui produit le raisonnement émergent.

#### 18.3 Compter les paramètres (culture utile)
Un paramètre ≈ 2 octets (fp16). Donc :
- 7 milliards de paramètres ≈ 14 Go → tourne sur un GPU 16-24 Go (quantifié).
- 70 milliards ≈ 140 Go → nécessite plusieurs GPU ou une quantification 4 bits.
**C'est pour ça qu'une IA locale au Burkina doit être quantifiée** (GGUF, 4 bits) ou très petite (1-3B).

#### 18.4 Minigrammaire du vocabulaire LLM (utile pour la suite)
| Terme | Sens simple |
|---|---|
| **Token** | morceau de mot (≈ 0,75 mot en anglais, ~2-3 caractères) |
| **Contexte** | nombre maximal de tokens que le modèle peut lire (8k, 32k, 128k…) |
| **Embedding** | vecteur de sens d'un token |
| **Self-attention** | chaque token pèse les autres tokens |
| **Prompt** | l'entrée qu'on donne |
| **Température** | créativité : 0 = très déterministe, 1+ = aléatoire |
| **Paramètres** | les « poids » appris (le savoir) |
| **Inférence** | l'utilisation du modèle (≠ entraînement) |
| **Quantification** | réduire la précision des poids (fp16 → int4) pour économiser la mémoire |
| **Fine-tuning** | réentraîner une partie des poids sur tes données |
| **LoRA / QLoRA** | fine-tuning économique (on n'entraîne que de petites matrices) |
| **Hallucination** | le modèle invente avec aplomb |
| **RAG** | donner au modèle des documents externes pour répondre juste |

#### 18.5 Code : regarder un Transformer en vrai (2 minutes)
```python
from transformers import AutoTokenizer, AutoModel
import torch

tok = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")
modele = AutoModel.from_pretrained("bert-base-multilingual-cased").eval()

texte = "L'IA peut aider l'agriculture au Sahel."
enc = tok(texte, return_tensors="pt")
with torch.no_grad():
    sortie = modele(**enc)
print("Tokens :", tok.convert_ids_to_tokens(enc["input_ids"][0])[:12])
print("Forme des représentations :", sortie.last_hidden_state.shape)  # (1, n_tokens, 768)
```

### ⚠️ Les 3 erreurs classiques
1. **Croire que le Transformer est toujours supérieur.** Sur 2 000 lignes tabulaires, un LightGBM gagne en 30 secondes de calcul.
2. **Confondre attention et explication.** Les poids d'attention ne sont pas une explication fiable — utilise SHAP/attention rollout avec prudence.
3. **Sous-estimer la donnée et le calcul.** Le Transformer a besoin de données ; sans pré-entraînement, il n'est pas magique.

### ✅ Quiz
1. Que représentent Q, K et V ?
2. Pourquoi divise-t-on par $\sqrt{d_k}$ ?
3. Pourquoi les Transformers utilisent-ils mieux les GPU que les RNN ?
4. Différence BERT / GPT ?
5. Qu'est-ce qu'un token, en une phrase ?

### 🛠️ Exercices
1. Avec `transformers`, extrais les embeddings de 5 phrases et calcule leurs similarités cosinus (compare « le chat dort » / « le chat se repose » à « la voiture roule »).
2. Classification de sentiment en français : `pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")` sur 10 avis. Commente les erreurs.
3. Écris 10 lignes expliquant l'attention à un non-technicien, avec une analogie de ton invention. (Excellent exercice d'entretien.)

---

# CHAPITRE 19 — Transfer learning et Hugging Face : faire grandir tes modèles

### 🎯 Objectif
Savoir réutiliser l'écosystème existant — la compétence la plus rentable du marché actuel. Personne n'entraîne un modèle depuis zéro en entreprise.

### 💡 L'essentiel en 5 minutes

**Transfer learning** : au lieu d'apprendre de zéro (des mois de GPU et des millions d'euros), tu prends un modèle **déjà entraîné** sur des masses de données, et tu l'**adaptes** à ton problème avec quelques milliers d'exemples.

Analogie : au lieu d'apprendre le français depuis la naissance, tu apprends le vocabulaire médical en 2 semaines — tu réutilises tout le reste.

### 📘 Le cours

#### 19.1 Les 3 niveaux d'adaptation
| Niveau | Ce qu'on fait | Coût | Quand |
|---|---|---|---|
| **Utilisation directe** | on appelle le modèle tel quel (API ou local) | 0 | sentiment, résumé, traduction, extraction |
| **Fine-tuning (LoRA)** | on réentraîne une petite partie | 1 h de GPU | tâche spécifique, données métier, style |
| **Entraînement complet** | on réentraîne tout | jours/semaines | rare, réservé aux labos |

#### 19.2 Le pipeline Hugging Face (3 lignes)
```python
from transformers import pipeline

sentiment = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
print(sentiment(["Ce modèle est excellent", "Le service client est catastrophique"]))
```
Autres pipelines immédiats : `summarization`, `translation`, `question-answering`, `ner` (entités nommées), `zero-shot-classification`, `automatic-speech-recognition`, `image-classification`, `object-detection`.

#### 19.3 Fine-tuning rapide avec le `Trainer`
```python
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
import numpy as np

ds = load_dataset("allocine")             # critiques de films en français
tok = AutoTokenizer.from_pretrained("distilbert-base-multilingual-cased")

def prep(ex):
    return tok(ex["review"], truncation=True, padding="max_length", max_length=256)

ds_tok = ds.map(prep, batched=True)
modele = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-multilingual-cased", num_labels=2)

def metriques(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)
    return {"accuracy": (preds == labels).mean()}

args = TrainingArguments(output_dir="out", num_train_epochs=2,
                         per_device_train_batch_size=16, eval_strategy="epoch",
                         learning_rate=2e-5, fp16=True, report_to="none")
trainer = Trainer(model=modele, args=args, train_dataset=ds_tok["train"],
                  eval_dataset=ds_tok["test"], compute_metrics=metriques)
trainer.train()
```
**Sur Colab (GPU gratuit), 1 000 exemples, 2 epochs → ~10 minutes.** Résultat typique : 90 %+ d'accuracy. **Mets ce notebook sur ton GitHub** : c'est un signal fort de compétence 2026.

#### 19.4 Signaux de reproductibilité (`model card`)
Pour chaque modèle pré-entraîné, vérifie : licence (commerciale ?), taille, langue supportée (français ?), benchmark, date, et si le modèle est « base » (à fine-tuner) ou « instruct » (prêt à discuter).

#### 19.5 Où sont les opportunités pour toi dès maintenant
1. **French NLP** : peu de modèles spécialisés en français d'Afrique (santé, agriculture, langues locales). Une niche réelle, avec un vrai potentiel d'impact et de publication.
2. **Langues locales** (mooré, dioula, fulfuldé) : quasi rien n'existe → contribution open source visible internationalement.
3. **Vision appliquée** : cultures, bétail, compteurs, documents administratifs.
4. **RAG métier** : moteur de recherche documentaire pour PME, ONG, cliniques (chapitre 21).

### ⚠️ Les 3 erreurs classiques
1. **Fine-tuner sans baseline** : commence par le modèle zéro-shot ou par une régression logistique. Souvent ça suffit.
2. **Utiliser un modèle anglais sur du français** : les scores chutent nettement. Choisis `multilingual`/`fr`.
3. **Ignorer la licence.** Un modèle « non commercial » ne peut pas partir en production dans une entreprise.

### ✅ Quiz
1. Qu'est-ce que le transfer learning, en une phrase ?
2. Que fait LoRA et pourquoi est-ce économique ?
3. Différence entre modèle « base » et « instruct » ?
4. Pourquoi vérifier la licence d'un modèle ?
5. Quel pipeline Hugging Face utiliserais-tu pour extraire les noms de médicaments d'ordonnances ?

### 🛠️ Exercices
1. Fine-tune un modèle multilingue sur un dataset français de ton choix (avis, spams SMS français, tweets santé). Compare à la baseline « toujours la classe majoritaire ».
2. Utilise `zero-shot-classification` pour trier 50 plaintes clients en 4 catégories sans données d'entraînement. Commente les limites.
3. **Projet fil rouge** : applique un modèle Hugging Face (texte ou vision) à ton domaine et note le gain par rapport à tes modèles de la Partie 2.

---

## 🏁 Fin de la Partie 3 : auto-évaluation

Tu es prêt pour la Partie 4 (LLM, RAG, déploiement) si tu peux :
- [ ] écrire une boucle d'entraînement PyTorch de mémoire (les 5 étapes) ;
- [ ] expliquer convolution, pooling et pourquoi un CNN bat un MLP en vision ;
- [ ] expliquer ce qu'est une série temporelle et pourquoi on ne mélange pas les dates ;
- [ ] dessiner un bloc Transformer et expliquer Q, K, V avec tes mots ;
- [ ] faire un fine-tuning Hugging Face et le présenter proprement ;
- [ ] dire **quand** tu ne utiliserais PAS le deep learning (la question piège classique).

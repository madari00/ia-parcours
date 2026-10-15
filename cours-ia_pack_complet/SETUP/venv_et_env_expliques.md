# 🧩 `.venv` ou `.env` ? Deux choses différentes (à ne jamais confondre)

> **La confusion est normale** : les deux s'appellent « environnement » et les deux commencent par un point.
> Mais elles n'ont **rien** en commun. Et se tromper là-dessus peut coûter très cher (fuite de clé d'API).

---

## Réponse immédiate

| Ma question | Réponse | Quand |
|---|---|---|
| Dois-je créer un **`.venv`** ? | **Oui, recommandé** | maintenant (5 minutes) |
| Dois-je créer un **`.env`** ? | **Non, pas maintenant** | **semaine 42** (projet RAG) |

---

## 1. Le tableau qui règle la question pour toujours

| | **`.venv`** (environnement virtuel) | **`.env`** (fichier de secrets) |
|---|---|---|
| **C'est quoi** | un dossier contenant une copie isolée de Python | un petit fichier texte avec des mots de passe |
| **Ça sert à** | que les bibliothèques d'un projet ne cassent pas les autres projets | ne pas écrire tes clés d'API dans ton code |
| **Ça contient** | des milliers de fichiers (numpy, pandas…) — plusieurs centaines de Mo | **2 à 5 lignes** de texte |
| **Créé avec** | `py -3.12 -m venv .venv` | un simple éditeur de texte (notepad, VS Code) |
| **Sur GitHub** | ignoré (`.gitignore`) — c'est trop lourd | **ignoré aussi, et c'est vital** — c'est un secret |
| **Tu en as besoin** | **maintenant** | **semaine 42** |

Autrement dit :
- **`.venv`** = ton **atelier** isolé → indispensable pour travailler proprement.
- **`.env`** = ton **coffre-fort** → utile uniquement quand tu as un secret à protéger.

---

## 2. `.venv` — l'environnement virtuel (à faire maintenant)

### Pourquoi
Imagine que tu installes la version 2 de `lightgbm` pour ton projet de la semaine 20… et qu'une autre application sur ton PC a besoin de la version 1. Sans isolation, **tout casse**. Le `.venv` donne à chaque projet son propre jeu de bibliothèques.

**Deuxième bénéfice, très concret :** tu peux supprimer un `.venv` et le recréer à l'identique à partir de `requirements.txt`. Ton projet devient **reproductible** — c'est-à-dire qu'il fonctionne aussi sur la machine de ton futur employeur. C'est exactement ce que fait le `Dockerfile` de tes projets de portfolio, en plus poussé.

### Les 4 commandes (Windows)
```powershell
cd C:\Users\issak\Documents\ia-parcours      # ton dossier de travail
py -3.12 -m venv .venv                        # 1. créer (une seule fois par projet)
.\.venv\Scripts\Activate.ps1                  # 2. activer (À CHAQUE nouvelle fenêtre)
python -m pip install --upgrade pip           # 3. mettre pip à jour
pip install numpy pandas matplotlib seaborn openpyxl ipykernel   # 4. installer les bibliothèques
```

**Le signe que ça marche :** ton prompt commence par `(.venv)`.
```
(.venv) PS C:\Users\issak\Documents\ia-parcours>
```

⚠️ **Piège fréquent :** si tu installes des bibliothèques **sans avoir activé** le `.venv`, elles partent dans le Python global et tu auras des « ModuleNotFoundError » incompréhensibles. Réflexe : **avant chaque séance, vérifie que tu vois `(.venv)`.**

### Si l'activation est bloquée
```
.\.venv\Scripts\Activate.ps1 : ... exécution de scripts est désactivée
```
→ Une seule fois : `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` → tape `O` → refais l'activation.

### ⚠️ Exceptions où on **n'utilise pas** de `.venv`
- **Dans Google Colab** : inutile, Colab est déjà un environnement isolé.
- Pour un script d'essai de 3 lignes que tu vas jeter : inutile.

---

## 3. `.env` — le fichier de secrets (semaine 42)

### Pourquoi
À la semaine 42, tu construiras ton **projet RAG**, qui appellera un modèle de langage. Tu auras alors une **clé d'API** : une longue chaîne de caractères qui **donne accès à ton compte, donc à ton argent**.

**Le danger, concrètement :** si tu écris cette clé dans un fichier `.py` et que tu fais `git push`, **elle est sur GitHub en 2 secondes**. Des robots scannent GitHub en permanence, et une clé volée peut générer des factures en quelques heures. Il arrive régulièrement que des développeurs — même expérimentés — se fassent vider un compte de cette façon.

**La règle :** une clé ne va **jamais** dans le code. Elle va dans un fichier `.env`, qui n'est **jamais** envoyé sur GitHub.

### Ce que ça donne (fichier `.env`, à la racine du projet)
```bash
MISTRAL_API_KEY=ta_vraie_cle_ici
OPENAI_API_KEY=sk-...
```

### Comment le code le lit
```python
import os
from dotenv import load_dotenv      # pip install python-dotenv

load_dotenv()                        # charge le fichier .env
cle = os.getenv("MISTRAL_API_KEY")   # récupère la clé, sans jamais l'écrire dans le code

if cle is None:
    raise SystemExit("Clé absente : vérifie ton fichier .env")
```

### Et surtout, dans `.gitignore`
```gitignore
.env
.env.*
!.env.example
```
*Traduction :* j'ignore `.env` et toutes ses variantes, **sauf** le modèle `.env.example` — qui, lui, doit être partagé (il montre à ton employeur quelles variables sont nécessaires, sans révéler les valeurs).

> ✅ Ce `.gitignore` est **déjà en place** dans le dépôt `modele_depot_ia-parcours/` que je t'ai fourni. Le fichier `.env.example` fourni dans ce dossier montre le format — tu le copieras en `.env` à la semaine 42.

### Les 4 règles à retenir pour toujours
1. **Jamais** de clé dans un fichier `.py`, `.ipynb`, ou `README`.
2. `.env` **toujours** dans `.gitignore` (à faire **avant** le premier commit du projet).
3. Un fichier **`.env.example`** avec des valeurs fictives → lui, il se versionne.
4. Si tu penses avoir poussé une clé par erreur : **révoque-la immédiatement** sur le site du fournisseur. Supprimer le fichier ne suffit pas — elle reste dans l'historique Git.

---

## 4. Le vocabulaire pour ne plus confondre (et briller en entretien)

| Le mot « environnement » peut désigner… | Exemple | Ce que c'est |
|---|---|---|
| **Environnement virtuel** | `.venv/` | isolation des bibliothèques Python |
| **Fichier d'environnement** | `.env` | stockage des secrets |
| **Variable d'environnement** | `os.environ["API_KEY"]` | valeur disponible pendant l'exécution |
| **Environnement de travail** | VS Code + Python + Git | l'ensemble de tes outils |
| **Environnement de production** | serveur en ligne | là où tourne l'application réelle |

**La phrase à savoir dire en entretien :**
> « J'utilise un environnement virtuel par projet pour garantir la reproductibilité, et je stocke les secrets dans un fichier `.env` exclu de Git — jamais dans le code. »

C'est une phrase courte qui prouve en 10 secondes que tu as déjà travaillé proprement. Beaucoup de juniors échouent sur ce point.

---

## 5. Ce que tu fais **aujourd'hui**

| Étape | Fichier | Fait ? |
|---|---|---|
| 1. Créer le `.venv` avec Python 3.12 | `.venv/` | à faire |
| 2. L'activer → prompt `(.venv)` | — | à faire |
| 3. Installer numpy, pandas, matplotlib… | — | à faire |
| 4. Créer un `.env` | `.env` | ❌ **rien à faire maintenant** |

**À la semaine 42 seulement**, quand tu attaqueras le RAG, tu feras :
```powershell
copy .env.example .env     # puis colle ta vraie clé dedans
```

D'ici là, tu n'as **aucune** clé d'API à gérer. Tu apprends sans compte payant, sans carte bancaire, sans secret à protéger.

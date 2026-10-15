# 🩺 DÉPANNAGE WINDOWS — erreurs fréquentes et solutions exactes

> Pour Windows 10 / 11 et PowerShell. Chaque erreur est traitée avec le message exact, la cause, et les commandes à copier.

---

## ⚡ Le réflexe n°1 (c'est la cause de 50 % des erreurs)

> **Après chaque installation d'un logiciel, FERME complètement la fenêtre PowerShell et rouvre-la.**

Windows ne met à jour la liste des programmes accessibles (le « PATH ») **qu'au démarrage d'un nouveau terminal**. Tant que tu gardes la même fenêtre ouverte, `git`, `python` ou `pip` peuvent continuer à être « non reconnus » alors qu'ils sont bien installés.

**Comment bien fermer :** clique sur la croix, ou tape `exit`. Ne te contente pas de minimiser.
**Ensuite :** `Windows` → tape `PowerShell` → Entrée.

---

## 1. ❌ « git n'est pas reconnu comme nom d'applet de commande »

```
git : Le terme «git» n'est pas reconnu comme nom d'applet de commande...
```

### La cause
**Un compte GitHub n'est pas le logiciel Git.** Ce sont deux choses différentes :
- **GitHub** = le site web (tes dépôts en ligne, ton profil). Tu l'as ✓.
- **Git** = le **logiciel** qui enregistre tes modifications sur **ta machine**. Il s'installe séparément. ✗ chez toi.

Sans Git installé, aucune commande `git …` ne fonctionnera, et tu ne pourras ni committer ni pousser.

### La solution (5 minutes)

**Méthode 1 — la plus simple (winget, inclus dans Windows 10/11) :**
```powershell
winget install --id Git.Git -e --source winget
```

**Méthode 2 — si winget ne fonctionne pas :**
1. Va sur **https://git-scm.com/download/win**
2. Le téléchargement démarre automatiquement (≈ 60 Mo)
3. Lance l'installateur et clique **« Next »** partout (les options par défaut sont bonnes)
4. À la fin : **décoche** « View Release Notes », clique **Finish**

### Vérification — dans une NOUVELLE fenêtre PowerShell
```powershell
git --version
```
Tu dois voir quelque chose comme : `git version 2.51.0.windows.1`

Si ça affiche encore « non reconnu » → tu n'as pas ouvert une nouvelle fenêtre. Ferme tout, rouvre, réessaie.

### Puis configure ton identité (indispensable)
```powershell
git config --global user.name "Issakha Daoud"
git config --global user.email "issakhadaoudabdelkerim95@gmail.com"
git config --global init.defaultBranch main
```

**Contrôle :**
```powershell
git config --global --list
```
Tu dois voir tes trois lignes.

> ⚠️ **Point crucial :** l'email doit être **exactement celui de ton compte GitHub** (et vérifié dans tes paramètres GitHub). C'est ce qui relie tes commits à ton profil. Avec le mauvais email, tes contributions n'apparaissent pas sur ton profil — et c'est justement ce que regardent les recruteurs.

> 💡 **Astuce :** Git pour Windows installe aussi **« Git Bash »**, un terminal où les commandes Linux fonctionnent (comme `ls`, `cat`). Beaucoup de tutos en ligne l'utilisent : c'est une bonne deuxième option si PowerShell te bloque.

---

## 1 bis. ❌ « git n'est pas reconnu » **après** avoir installé Git

C'est le cas le plus déroutant : tu as bien lancé l'installation, et `git` reste introuvable. Il y a **3 causes possibles**, et un test de 30 secondes pour savoir laquelle.

### 🔎 Le test qui tranche (30 secondes)

**Ouvre un terminal PowerShell EN DEHORS de VS Code :**
appuie sur `Windows + X` → **« Terminal »** (ou « Windows PowerShell »).

Puis tape :
```powershell
git --version
```

| Résultat | Cause | Solution |
|---|---|---|
| ✅ Ça affiche `git version 2.x` | **Cause B** : VS Code n'a pas redémarré | voir ci-dessous |
| ❌ « non reconnu » aussi | **Cause A** : Git n'est pas installé — ou **Cause C** : pas dans le PATH | lancer `diagnostic_git.ps1` |

---

### 🅱️ Cause B — VS Code n'a pas été redémarré **complètement** (la plus fréquente)

**Ce qui se passe :** quand tu ouvres un terminal dans VS Code, ce terminal reçoit la liste des logiciels (le « PATH ») **telle que VS Code l'a capturée au moment de son démarrage**. Installer Git pendant que VS Code est ouvert ne change rien pour lui : il continue d'utiliser l'ancienne liste.

⚠️ **Ouvrir un nouvel onglet de terminal ne suffit pas.** Ni « Terminal → Nouveau terminal », ni même « Developer: Reload Window ». Le processus principal de VS Code est lancé, il garde son vieux PATH.

**La solution :**
1. Ferme **TOUTES** les fenêtres VS Code (vérifie la barre des tâches : il y en a souvent une deuxième oubliée).
2. Rouvre VS Code.
3. Ouvre un nouveau terminal (`Ctrl` + `` ` ``).
4. Tape :
```powershell
git --version
```

> 💡 **Le réflexe à garder pour toute ta carrière :** après avoir installé un logiciel (Git, Python, Node, Docker…), **ferme et rouvre ton terminal** — et si tu es dans VS Code, ferme et rouvre **VS Code entier**. C'est la cause n°1 des « mais je l'ai installé pourtant ! ».

---

### 🅰️ Cause A — Git n'est pas réellement installé

Vérifie dans l'Explorateur de fichiers (`Windows + E`) si ce dossier existe :
```
C:\Program Files\Git
```
- **Le dossier existe** → Git est installé, va voir la Cause C.
- **Le dossier n'existe pas** → Git n'est pas installé. Refaire l'installation :
```powershell
winget install --id Git.Git -e --source winget
```
Lis bien ce que répond `winget` : si tu vois `Successfully installed`, c'est bon. Si tu vois une erreur (ou `winget` non reconnu), utilise l'installateur manuel : https://git-scm.com/download/win → lance le fichier téléchargé → « Next » partout → **Install** → attends la fin (la barre doit arriver à 100 %) → Finish.

> ⚠️ **Piège classique :** télécharger le fichier d'installation **sans le lancer**. Le fichier est dans `Téléchargements`, mais tant que tu n'as pas cliqué dessus et terminé l'assistant, **rien n'est installé**. Un `winget install` qui affiche une erreur du même type arrive aussi : dans ce cas, méthode manuelle.

---

### 🅲 Cause C — Git est installé mais absent du PATH

Symptôme : le dossier `C:\Program Files\Git` existe, mais `git` n'est pas reconnu.

**Solution propre** — ouvre PowerShell et colle ces deux lignes (elles ajoutent Git au PATH **de ton compte utilisateur** uniquement, sans toucher au système) :
```powershell
$p = [Environment]::GetEnvironmentVariable('Path','User')
[Environment]::SetEnvironmentVariable('Path', $p + ';C:\Program Files\Git\cmd', 'User')
```
Puis **ferme et rouvre VS Code** et teste `git --version`.

> ⚠️ N'utilise pas la commande `setx PATH "%PATH%;..."` trouvée sur certains forums : elle **tronque** le PATH à 1024 caractères et peut casser d'autres logiciels. Le script PowerShell ci-dessus est la bonne méthode.
>
> 💡 Si Git est installé ailleurs (par exemple dans ton dossier utilisateur), adapte le chemin. Le script `diagnostic_git.ps1` fourni te donne le chemin exact à utiliser.

---

### 🔧 En un clic : le script de diagnostic

Dans le dossier `SETUP/` je t'ai mis **`diagnostic_git.ps1`**. Il te dit en 5 secondes où est le problème :

```powershell
powershell -ExecutionPolicy Bypass -File diagnostic_git.ps1
```
*(ou : clic droit sur le fichier → « Exécuter avec PowerShell »)*

Il vérifie : la commande `git`, les emplacements d'installation habituels, les entrées Git dans ton PATH, et affiche **la solution exacte** à copier selon ton cas.

---

## 2. ⚠️ Python 3.14 est trop récent pour ce parcours

### Comment le repérer
Dans tes chemins d'installation :
```
C:\Users\issak\AppData\Local\Programs\Python\Python314\
                                                  ↑↑
                                            Python 3.14
```

### Pourquoi c'est un problème (plus tard)
Python 3.14 est très récent. **la Partie 1 (semaines 1-13) fonctionne parfaitement dessus** — ton installation actuelle est bonne pour apprendre Pandas et NumPy.

En revanche, les bibliothèques des **Parties 2, 3 et 4** doivent être compilées pour chaque version de Python. Certaines n'ont pas encore de version compatible 3.14 :

| Bibliothèque | Utilisée à partir de | Statut sur Python 3.14 |
|---|---|---|
| numpy, pandas, matplotlib | Partie 1 | ✓ installés, ça marche |
| scikit-learn, joblib | semaine 14 | probablement ✓ |
| **LightGBM, XGBoost** | semaine 20 | ⚠️ à vérifier |
| **SHAP** | semaine 24 | ⚠️ à vérifier |
| **PyTorch, torchvision** | semaine 27 | ⚠️ risque élevé |
| **transformers, datasets** | semaine 38 | ⚠️ risque élevé |
| **FAISS, sentence-transformers** | semaine 42 | ⚠️ risque élevé |

### La solution : installer **Python 3.12** à côté

Windows accepte plusieurs versions en parallèle — **ton 3.14 reste intact**, on ajoute simplement une version mieux supportée.

```powershell
winget install --id Python.Python.3.12 -e
```
*(ou téléchargement manuel : https://www.python.org/downloads/release/python-3129/ → « Windows installer (64-bit) »)*

⚠️ **Pendant l'installation manuelle : coche « Add python.exe to PATH »** en bas de la première fenêtre.

**Puis FERME et ROUVRE PowerShell**, et vérifie :
```powershell
py -0
```
Tu dois voir la liste de tes versions :
```
 -V:3.14 *        Python 3.14 (64-bit)
 -V:3.12          Python 3.12 (64-bit)
```
Le `*` indique celle utilisée par défaut — ce n'est pas grave.

> 💡 **`py` est le lanceur Python de Windows.** Il te permet de choisir la version :
> `py -3.12 mon_script.py` utilise 3.12, `py -3.14 mon_script.py` utilise 3.14.
> Retiens surtout : **pour tout ce parcours, utilise `py -3.12`.**

---

## 3. ✅ Créer ton environnement de travail avec Python 3.12

C'est à faire **une fois**, dans le dossier de ton parcours.

### 3.1 Crée l'environnement virtuel
```powershell
# 1. Va dans ton dossier de travail
cd C:\Users\issak\Documents\ia-parcours     # (voir section 5 pour le créer)

# 2. Crée l'environnement avec Python 3.12
py -3.12 -m venv .venv

# 3. Active-le
.\.venv\Scripts\Activate.ps1
```

Après l'activation, ton prompt change et affiche `(.venv)` au début :
```
(.venv) PS C:\Users\issak\Documents\ia-parcours>
```
**C'est le signe que ça marche.** Tout ce que tu installes maintenant sera isolé dans ce dossier.

⚠️ **Il faut activer l'environnement à chaque nouvelle fenêtre PowerShell** avant de travailler.

### 3.2 Si PowerShell refuse : « running scripts is disabled »
```
.\.venv\Scripts\Activate.ps1 : ... exécution de scripts est désactivée sur ce système
```
Solution (une seule fois) :
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```
Tape `O` (ou `Y`) puis Entrée. Relance l'activation.

**Alternative sans rien changer :** utilise l'invite de commandes `cmd` au lieu de PowerShell, et tape `.venv\Scripts\activate.bat`.

### 3.3 Installe les bibliothèques de la Partie 1 dans cet environnement
```powershell
python -m pip install --upgrade pip
pip install numpy pandas matplotlib seaborn openpyxl ipykernel
```

### 3.4 Vérifie que tout est prêt
```powershell
python verifier_environnement.py
```
*(le fichier est dans `SETUP/`. Si tu es dans un autre dossier : `python SETUP\verifier_environnement.py`)*

Tu dois voir des ✓ sur la ligne **T1 · Fondations**, et git configuré.

---

## 4. Tableau récapitulatif : message d'erreur → solution

| Message PowerShell | Cause | Solution |
|---|---|---|
| `Le terme «git» n'est pas reconnu` | Git non installé | `winget install --id Git.Git -e` puis **rouvrir le terminal** |
| `Le terme «python» n'est pas reconnu` | Python absent ou pas dans le PATH | réinstaller en cochant « Add to PATH » |
| `Le terme «pip» n'est pas reconnu` | pip absent du PATH | utilise `python -m pip install …` |
| `Le terme «code» n'est pas reconnu` | VS Code pas dans le PATH | VS Code → `Ctrl+Shift+P` → « Shell Command: Install 'code' command in PATH » |
| `running scripts is disabled` | politique PowerShell | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| `error: externally-managed-environment` | environnement géré par le système | active ton `.venv` (section 3.1) |
| `pip : commande introuvable` dans un venv | venv non activé | `.\.venv\Scripts\Activate.ps1` |
| `fatal: not a git repository` | tu n'es pas dans un dossier Git | `git init` d'abord |
| `failed to push some refs` | le dépôt GitHub contient déjà des fichiers | recrée un dépôt **vide** (sans README) ou fais `git pull --rebase origin main` |
| `ModuleNotFoundError: No module named 'X'` | paquet non installé (ou mauvais Python) | `pip install X` **puis** vérifie que le venv est actif |

---

## 5. Bonus : où mettre tes fichiers (et pourquoi pas « Downloads »)

Ton dossier est actuellement dans `C:\Users\issak\Downloads\cours_ia`. **Downloads est nettoyé** par les outils de nettoyage Windows et tu risques de perdre ton travail.

**Déplace-le vers Documents (méthode simple) :**
1. Ouvre l'Explorateur de fichiers (`Windows + E`)
2. Va dans `Téléchargements`, clic droit sur le dossier `cours_ia` → **Couper**
3. Va dans `Documents`, clic droit dans le vide → **Coller**
4. Renomme-le `ia-parcours` (clic droit → Renommer)

Ensuite, dans PowerShell :
```powershell
cd C:\Users\issak\Documents\ia-parcours
```

> 💡 Ce dossier deviendra ton dépôt Git : il contiendra ton code, ton carnet, et tes 4 projets de portfolio. Il mérite un emplacement sûr — et pense à faire `git push` à chaque fin de séance (c'est ta sauvegarde).

---

## 6. Ta séquence exacte, dans l'ordre (à faire maintenant)

```powershell
# ── ÉTAPE 1 : installer Git ──────────────────────────────────
winget install --id Git.Git -e --source winget

# ── ÉTAPE 2 : FERMER POWERSHELL ET LE ROUVRIR ────────────────
# (indispensable)

# ── ÉTAPE 3 : vérifier et configurer Git ─────────────────────
git --version
git config --global user.name "Issakha Daoud"
git config --global user.email "issakhadaoudabdelkerim95@gmail.com"
git config --global init.defaultBranch main
git config --global --list

# ── ÉTAPE 4 : installer Python 3.12 ──────────────────────────
winget install --id Python.Python.3.12 -e

# ── ÉTAPE 5 : FERMER POWERSHELL ET LE ROUVRIR ────────────────

# ── ÉTAPE 6 : vérifier les deux versions ─────────────────────
py -0

# ── ÉTAPE 7 : se placer dans le dossier du parcours ──────────
cd C:\Users\issak\Documents\ia-parcours

# ── ÉTAPE 8 : créer et activer l'environnement 3.12 ──────────
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1        # si ça bloque : Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

# ── ÉTAPE 9 : installer les bibliothèques de la Partie 1 ─────
python -m pip install --upgrade pip
pip install numpy pandas matplotlib seaborn openpyxl ipykernel

# ── ÉTAPE 10 : tout vérifier ─────────────────────────────────
python SETUP\verifier_environnement.py
```

**Et ensuite ?** Ton premier exercice :
```powershell
python semaine_01\exercice_convertisseur.py
```
*(le fichier est dans `SETUP\modele_depot_ia-parcours\` — copie son contenu dans ton dossier de travail si tu ne l'as pas déjà fait)*

---

## 7. Checklist finale

- [ ] `git --version` répond (dans une **nouvelle** fenêtre PowerShell)
- [ ] `git config --global --list` affiche ton nom + l'email de ton compte GitHub
- [ ] `py -0` liste **3.12** et 3.14
- [ ] Le prompt affiche `(.venv)` après activation
- [ ] `python --version` affiche **3.12.x** quand le venv est actif
- [ ] `python SETUP\verifier_environnement.py` → ✓ partout en Partie 1
- [ ] Le dossier de travail est dans `Documents`, pas dans `Downloads`

**Si un message d'erreur résiste : copie-le ici tel quel. Ne le résume pas — le texte exact contient l'information dont j'ai besoin.**

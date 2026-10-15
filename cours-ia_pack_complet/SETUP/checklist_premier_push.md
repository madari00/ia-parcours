# 🚦 CHECKLIST — du terminal au premier `git push`

> **Ton état actuel (mis à jour) :** Git 2.56 ✓ · dossier déplacé dans `C:\Users\issak\cours_ia` ✓ · `.venv` créé dans `Downloads` puis **déplacé** ⚠️ · pseudo GitHub : **madari00**
>
> Deux choses à corriger avant ton premier commit. Durée : **5 minutes.**

---

## ⚠️ Les 3 pièges à régler maintenant

| # | Problème | Pourquoi c'est grave |
|---|---|---|
| 1 | Le dossier est dans `C:\Users\issak\Downloads\` | Windows **nettoie** périodiquement le dossier Téléchargements → risque de perdre ton dépôt et tes projets |
| 2 | Tes bibliothèques (numpy, pandas…) sont dans le **Python global 3.14**, pas dans le `.venv` | Ton projet ne sera **pas reproductible** et tu auras des `ModuleNotFoundError` difficiles à comprendre |
| 3 | Le `.venv` a peut-être été créé avec **Python 3.14** | Les bibliothèques des Parties 2 à 4 risquent de ne pas s'installer |

Bonne nouvelle : **les trois se règlent d'un coup**, en recréant le `.venv` au bon endroit. 2 minutes.

---

## 🅰️ ÉTAPE 1 — Vérifier ta configuration Git (30 secondes)

Dans le terminal VS Code (tu dois voir `(.venv)`) :
```powershell
git config --global --list
```

**Ce que tu dois voir :**
```
user.name=Issakha Daoud
user.email=issakhadaoudabdelkerim95@gmail.com
init.defaultbranch=main
```

❓ **Si tu ne vois rien, ou seulement une partie** : tes 3 commandes ont peut-être été mal interprétées quand tu les as collées en bloc (tu as vu les `>>` dans ton terminal). Retape-les **une ligne à la fois**, en appuyant sur `Entrée` après chacune :
```powershell
git config --global user.name "Issakha Daoud"
git config --global user.email "issakhadaoudabdelkerim95@gmail.com"
git config --global init.defaultBranch main
```
💡 `git config` **n'affiche rien** quand ça réussit : le silence est normal. La preuve, c'est `git config --global --list`.

---

## 🅱️ ÉTAPE 2 — Ton `.venv` a été déplacé : à recréer

**Ce qui s'est passé :** ton `.venv` a été créé dans `Downloads\cours_ia\.venv`, puis le dossier a été **déplacé** vers `C:\Users\issak\cours_ia`. Le venv s'active encore (le prompt affiche `(.venv)`), mais il garde en interne les **anciens chemins** et probablement **Python 3.14**.

**Comment le vérifier toi-même** — le script de diagnostic le détecte maintenant automatiquement :
```powershell
python SETUP\verifier_environnement.py
```
Il affichera, dans la section 1 :
```
venv base : Python 3.14.x  (C:\...\Python314)
⚠ cet environnement a été créé avec Python 3.14.x
⚠ ce venv a été DÉPLACÉ depuis sa création.
```

**Pourquoi ça compte :** un venv est lié à son emplacement et à sa version de Python. Déplacé, il peut fonctionner « presque » — et échouer bizarrement au moment le plus gênant (installation d'une bibliothèque à la semaine 20). On le recrée donc proprement : **2 minutes**, et pip réutilise son cache (rien à re-télécharger).

→ Voir l'**étape 3** ci-dessous, qui est la seule à faire.

## 🅲 ÉTAPE 3 — Recréer le `.venv` proprement (2 minutes)

Le venv actuel est lié à l'ancien chemin et au mauvais Python. On le refait — c'est plus rapide que de le réparer.

Dans le terminal VS Code (nouveau dossier, donc plus de `(.venv)`) :

```powershell
# 1. Supprimer l'ancien venv mal placé (dans Téléchargements)
Remove-Item -Recurse -Force C:\Users\issak\Downloads\cours_ia\.venv

# 2. Se placer dans le dossier déplacé
cd C:\Users\issak\Documents\ia-parcours

# 3. Vérifier quelles versions de Python tu as
py -0
```

### Selon ce que renvoie `py -0`

**Cas 1 — tu vois `-V:3.12` :**
```powershell
py -3.12 -m venv .venv
```

**Cas 2 — tu ne vois que `-V:3.14`** (tu n'as pas encore installé 3.12) :
```powershell
winget install --id Python.Python.3.12 -e
# FERME et ROUVRE VS Code, puis :
cd C:\Users\issak\Documents\ia-parcours
py -3.12 -m venv .venv
```

### Active et installe (dans tous les cas)
```powershell
.\.venv\Scripts\Activate.ps1
# le prompt doit afficher (.venv)

python --version                 # doit afficher 3.12.x
python -m pip install --upgrade pip
pip install numpy pandas matplotlib seaborn openpyxl ipykernel
```

> 💡 **Rapide** : pip réutilise les fichiers déjà téléchargés (cache). Il n'y aura pas 37 Mo à re-télécharger.

### Vérifie que tu es dans le bon environnement
```powershell
python -c "import sys; print(sys.prefix)"
```
Le chemin affiché doit contenir `ia-parcours\.venv`. **C'est la preuve que tu installes au bon endroit.**

---

## 🅳 ÉTAPE 4 — Diagnostic complet

```powershell
python SETUP\verifier_environnement.py
```

Attendu : des ✓ partout sur **T1 · Fondations**, l'identité Git détectée, et un ✓ sur le venv actif.
Les ✗ des phases T2/T3/T4 sont **normaux** — on les installe en temps voulu.

---

## 🅴 ÉTAPE 5 — Ton premier dépôt Git

### 5.1 Crée le dépôt vide sur GitHub (**avant** de pousser)
1. Va sur **github.com** → connecte-toi
2. Bouton **`+`** en haut à droite → **New repository**
3. **Repository name** : `ia-parcours`
4. Description : `Mon parcours d'apprentissage en data science et IA appliquée`
5. ⚠️ **Ne coche RIEN** : ni « Add a README », ni « Add .gitignore », ni « Choose a license »
6. **Create repository**

> ⚠️ **Crucial : le dépôt doit être VIDE.** Si tu ajoutes un README, GitHub crée son propre commit et ton `git push` sera **refusé** (« failed to push some refs »).

### 5.2 Initialise et pousse (dans VS Code, prompt `(.venv)`)
```powershell
git init
git add .
git commit -m "feat: initialise mon parcours IA"
git branch -M main
git remote add origin https://github.com/madari00/ia-parcours.git
git push -u origin main
```
*(`madari00` = ton pseudo GitHub, confirmé sur ton profil)*

### 5.3 Ce qui va se passer au premier `push`

**Une fenêtre de navigateur va s'ouvrir** pour te connecter à GitHub (c'est le **Git Credential Manager**, inclus avec Git for Windows). Connecte-toi, autorise, et c'est terminé — **une seule fois**.

Si au lieu de ça le terminal te demande un **mot de passe** : GitHub **refuse les mots de passe**. Il faut un **jeton d'accès personnel** :
1. GitHub → photo de profil → **Settings** → **Developer settings** (tout en bas)
2. **Personal access tokens** → **Tokens (classic)** → **Generate new token (classic)**
3. Note : `git-windows`, Expiration : 90 jours
4. Coche la case **`repo`** (obligatoire)
5. **Generate token** → **copie le jeton** (tu ne le verras plus jamais)
6. Au moment du `push` : identifiant = ton pseudo GitHub, **mot de passe = colle le jeton**

> 🔐 Ce jeton est un secret : ne le colle jamais dans un fichier, ni dans un chat, ni sur GitHub.

### 5.4 Vérifie
Actualise la page de ton dépôt GitHub : tu dois voir tes fichiers (README.md, carnet.md, semaine_01/…).
Et en local :
```powershell
git log --oneline
git status
```
`git status` doit afficher : *nothing to commit, working tree clean* et *Your branch is up to date with 'origin/main'*.

---

## 🅵 ÉTAPE 6 — Ton premier exercice versionné

```powershell
python semaine_01\exercice_convertisseur.py
```

*(si le fichier n'y est pas encore, copie-le depuis `SETUP\modele_depot_ia-parcours\semaine_01\`)*

**Attendu :**
```
10 000 FCFA = 15.24 EUR
50 000 FCFA = 76.22 EUR
250 000 FCFA = 381.12 EUR
1 000 000 FCFA = 1 524.49 EUR

✅ Tous les tests passent.
```

Puis **le réflexe à garder à vie** — à la fin de **chaque** séance de travail :
```powershell
git add .
git commit -m "feat: ajoute le prix au kilo au convertisseur"
git push
```

> 💡 Trois commandes, 15 secondes. C'est ta sauvegarde **et** la preuve publique de ta régularité — exactement ce que regardera un recruteur dans 10 mois.

---

## ✅ Checklist finale : tu es lancé quand…

- [ ] `git config --global --list` affiche ton nom, ton email et `main`
- [ ] Le dossier est dans `C:\Users\issak\Documents\ia-parcours`
- [ ] `python --version` affiche **3.12.x** (avec `(.venv)` dans le prompt)
- [ ] `python -c "import sys; print(sys.prefix)"` contient `ia-parcours\.venv`
- [ ] `python SETUP\verifier_environnement.py` → ✓ sur T1 · Fondations
- [ ] Le dépôt `ia-parcours` est visible sur GitHub avec tes fichiers
- [ ] `python semaine_01\exercice_convertisseur.py` affiche « ✅ Tous les tests passent »
- [ ] La semaine 1 est **cochée** dans `plan_etude.html` (ouvert dans un **navigateur**)

**Les 8 cases cochées = tu as franchi la partie administrative. Semaine 2 : les bases de Python.** 🚀

---

## 🆘 En cas de blocage

| Message | Solution |
|---|---|
| `failed to push some refs` | ton dépôt GitHub n'était pas vide → supprime-le et recrée-le **vide** |
| `remote origin already exists` | `git remote set-url origin https://github.com/madari00/ia-parcours.git` |
| `Permission denied (publickey)` | utilise l'URL **https** (pas `git@github.com:...`) |
| `src refspec main does not match any` | tu n'as pas encore fait de `git commit` |
| `ModuleNotFoundError` | tu n'as pas activé le venv : `.\.venv\Scripts\Activate.ps1` |
| `exécution de scripts est désactivée` | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` (une fois) |

**Bloqué ? Colle ici le message d'erreur complet, sans le résumer.**

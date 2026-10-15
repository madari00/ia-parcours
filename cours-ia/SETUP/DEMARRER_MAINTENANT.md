# 🚀 DÉMARRER MAINTENANT — la fiche d'une page

> Tu as **VS Code ✓ · Python ✓ · GitHub ✓**.
> Il te reste **2 commandes** à lancer. C'est tout. Lecture : 3 minutes.

---

## 1. Quelle application ouvre quel fichier (à retenir)

| Fichier du pack | Bonne application | Remarque |
|---|---|---|
| `*.md` (cours, fiches) | **VS Code** | normal que ça s'ouvre là ✅ — mais appuie sur **`Ctrl+Shift+V`** pour l'afficher **mis en forme** au lieu du texte brut |
| `plan_etude.html` | **Navigateur** (Chrome / Edge / Firefox) | ⚠️ **pas VS Code** : les cases à cocher et la progression ont besoin d'un navigateur |
| `simulateur_rythme.html` | **Navigateur** | idem |
| `*.ipynb` (notebooks) | **VS Code** ou **Google Colab** | dans VS Code, il faut l'extension Jupyter (section 3) |
| `CV_....docx` | **Word**, **LibreOffice** ou **Google Docs** | pas VS Code |
| `*.py` (code) | **VS Code** | exécution : bouton ▶ en haut à droite |

### L'astuce VS Code pour lire le cours confortablement
1. Ouvre un fichier `.md` dans VS Code.
2. Appuie sur **`Ctrl` + `Shift` + `V`** → le texte s'affiche **mis en forme** (titres, tableaux, gras).
3. Pour lire le cours **et** coder côte à côte : **`Ctrl` + `K`** puis **`V`** → aperçu à droite, code à gauche.
4. Pour naviguer dans un long fichier : **`Ctrl` + `Shift` + `O`** affiche le sommaire des titres.

**Extension optionnelle mais agréable** (meilleur rendu des tableaux et formules) :
```bash
code --install-extension shd101wyy.markdown-preview-enhanced
```

---

## 2. Ce que tu installes MAINTENANT (Partie 1)

### Réponse courte
Pour les **semaines 2 à 4** (Python pur : variables, boucles, fonctions, fichiers) : **RIEN.** Ton Python actuel suffit. Tu peux commencer ce soir.

Pour être tranquille jusqu'à la **semaine 13**, une seule commande installe tout (≈ **37 Mo** de téléchargement) :

```bash
pip install numpy pandas matplotlib seaborn openpyxl ipykernel
```

### Détail de ce que tu installes (et pourquoi)

| Paquet | Taille | À quoi il sert | Tu l'utilises à partir de |
|---|---|---|---|
| `numpy` | ~18 Mo | tableaux, calcul vectoriel, matrices | **semaine 5** |
| `pandas` | ~12 Mo | lire et nettoyer les données (CSV, Excel) | **semaine 7** |
| `matplotlib` | ~8 Mo | graphiques et visualisations | **semaine 5** |
| `seaborn` | ~1 Mo | graphiques statistiques (facilite matplotlib) | **semaine 8** |
| `openpyxl` | ~0,3 Mo | lire les fichiers Excel (.xlsx) | **semaine 7** |
| `ipykernel` | ~1 Mo | **exécuter les notebooks `.ipynb` dans VS Code** | dès que tu ouvres `01_premiers_pas_python.ipynb` |

> ℹ️ **Pas besoin de `jupyterlab`** : tu as VS Code + l'extension Jupyter, ce qui remplace Jupyter Notebook classique (`ipykernel` suffit).
> ℹ️ **Pas besoin de Colab pour la Partie 1** : tout tourne en local sans GPU. Garde Colab pour le deep learning (semaine 27+).

### Si ta connexion est lente
Coupe la commande en deux, tu peux t'arrêter entre les deux :
```bash
pip install numpy pandas matplotlib        # le gros du téléchargement
pip install seaborn openpyxl ipykernel     # le reste, très léger
```

---

## 3. Les 3 réglages VS Code (5 minutes)

> 🩺 **Erreur « le terme git n'est pas reconnu » ?** Un **compte GitHub n'est pas le logiciel Git** — il faut l'installer séparément.
> Tout est traité dans **`DEPANNAGE_WINDOWS.md`, section 1** (avec la commande exacte). Et si tu as **Python 3.13 ou 3.14**, lis la section 2 de ce même fichier : ça t'évitera un blocage à la semaine 20.

### 3.1 Configurer ton identité Git — **le plus important**
```bash
git config --global user.name "Prenom Nom"
git config --global user.email "l'email de ton compte GitHub"
git config --global init.defaultBranch main
```
⚠️ Sans ça, **tous tes commits sont anonymes** et n'apparaissent pas sur ton profil GitHub. Or c'est la première chose qu'un recruteur technique regarde pour vérifier que tu codes vraiment. Mets **l'email associé à ton compte GitHub**.

### 3.2 Installer les extensions (à coller dans le terminal VS Code)
```bash
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension ms-toolsai.jupyter
code --install-extension charliermarsh.ruff
code --install-extension eamodio.gitlens
```
Si `code` n'est pas reconnu : dans VS Code, `Ctrl+Shift+P` → tape **« Shell Command: Install 'code' command in PATH »** → Entrée. Puis relance le terminal.

### 3.3 Vérifier que tout est bon
```bash
python ../SETUP/verifier_environnement.py
```
*(ou, depuis le dossier `SETUP` : `python verifier_environnement.py`)*

Tu dois voir des ✓ sur la section **T1 · Fondations**. Les ✗ des autres phases sont **normaux** — on les installe plus tard, au moment utile.

---

## 4. Ton premier exercice (15 minutes, maintenant)

**Option A — dans VS Code (recommandé, tu apprends le vrai flux de travail)**
```bash
# 1. Copie le dossier modèle dans un espace de travail
#    (place-le où tu veux, par exemple Documents/ia-parcours)

# 2. Ouvre-le dans VS Code
code chemin/vers/ia-parcours

# 3. Lance le premier script : clique sur ▶ en haut à droite du fichier
#    semaine_01/exercice_convertisseur.py
```
Tu dois voir s'afficher :
```
10 000 FCFA = 15.24 EUR
50 000 FCFA = 76.22 EUR
250 000 FCFA = 381.12 EUR
1 000 000 FCFA = 1 524.49 EUR

✅ Tous les tests passent.
```

**Option B — en ligne de commande** : `python semaine_01/exercice_convertisseur.py`

### Puis publie-le sur GitHub (ton livrable de la semaine 1)
```bash
cd ia-parcours
git init
git add .
git commit -m "feat: initialise mon parcours IA et le premier exercice"
git branch -M main
git remote add origin https://github.com/TON-PSEUDO/ia-parcours.git
git push -u origin main
```
*(Crée d'abord le dépôt vide `ia-parcours` sur github.com — **sans** cocher « Add a README », sinon le `push` sera refusé.)*

---

## 5. Ta checklist « je peux commencer »

- [ ] `python --version` affiche **3.10** ou plus
- [ ] `pip install numpy pandas matplotlib seaborn openpyxl ipykernel` terminé sans erreur rouge
- [ ] `git config --global user.name` et `user.email` renseignés
- [ ] Les 5 extensions VS Code installées
- [ ] `python verifier_environnement.py` → tout ✓ sur la ligne **T1 · Fondations**
- [ ] `semaine_01/exercice_convertisseur.py` s'exécute et affiche « ✅ Tous les tests passent »
- [ ] Dépôt `ia-parcours` poussé sur GitHub
- [ ] `carnet.md` ouvert dans un onglet VS Code (à remplir à chaque séance)
- [ ] Semaine 1 **cochée** dans `plan_etude.html` (à ouvrir dans ton **navigateur**)

**Quand ces 9 cases sont cochées, tu as dépassé 90 % des gens qui « veulent apprendre l'IA ». Semaine 2 : les bases de Python.**

---

## 6. Les 5 erreurs de débutant à éviter dès maintenant

| Erreur | Ce qui se passe | À faire |
|---|---|---|
| Modifier le Python système / accumuler les installations | conflits de versions, tout casse | une seule installation Python, propre |
| Travailler **sans** `git commit` régulier | perte de travail, historique vide | commit à **chaque fin de séance** |
| Mettre une clé d'API dans un fichier `.py` | elle part sur GitHub en 2 secondes | variable d'environnement + `.env` dans `.gitignore` |
| Ouvrir `plan_etude.html` dans VS Code | rien ne s'affiche correctement | ouvre-le dans **Chrome / Firefox** |
| Installer PyTorch maintenant | 2 Go téléchargés pour rien pendant 5 mois | attends la **semaine 27** |

---

*Besoin d'un coup de main ? Dis-moi exactement quel message d'erreur s'affiche, et je te donne la correction.*

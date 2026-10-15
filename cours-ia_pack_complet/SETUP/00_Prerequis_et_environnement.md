# 🔧 PRÉREQUIS ET ENVIRONNEMENT DE TRAVAIL

> **Ta situation :** VS Code ✓ · Python ✓ · compte GitHub ✓
> **Donc cette page se résume à :** 10 minutes de configuration, puis tu commences la semaine 1. Ne saute pas la section 2 : trois réglages t'éviteront des heures de frustration.

---

> 🩺 **Un problème d'installation ?** → **`DEPANNAGE_WINDOWS.md`** traite les erreurs réelles :
> « git n'est pas reconnu », « running scripts is disabled », Python 3.14 trop récent, `pip` introuvable, dossier dans Téléchargements… avec les commandes exactes à copier.

---

## 1. Ce que tu as déjà (rien à faire)

| Élément | État | Utilisation dans le parcours |
|---|---|---|
| **VS Code** | ✓ | ton éditeur principal : notebooks, scripts, Git intégré |
| **Python** | ✓ | à vérifier : version ≥ 3.10 (voir section 2) |
| **Compte GitHub** | ✓ | ton CV technique : dépôt `ia-parcours` + 4 projets de portfolio |

C'est l'essentiel. **Tout le reste s'installe progressivement, phase par phase** (section 4).

---

## 2. Les 3 réglages à faire maintenant (10 minutes)

### 2.1 Vérifier ta version de Python
Ouvre un terminal dans VS Code (`Ctrl` + `` ` ``) :
```bash
python --version        # Windows : python --version  ou  py --version
```
- Si c'est **≥ 3.10** → parfait.
- Si c'est **3.8 ou moins** → installe la version 3.11 ou 3.12 depuis python.org. Les bibliothèques d'IA (LightGBM, PyTorch, transformers) abandonnent les vieilles versions.

### 2.2 Configurer ton identité Git (obligatoire — 30 secondes)
Sans ça, **tous tes commits sont anonymes** et tes contributions ne t'identifient pas. C'est le réglage le plus souvent oublié.
```bash
git config --global user.name "Prenom Nom"
git config --global user.email "l'email de ton compte GitHub"
git config --global init.defaultBranch main

# Vérifie :
git config --global --list
```
> 💡 Utilise **l'email associé à ton compte GitHub**. Sinon GitHub ne reliera pas tes commits à ton profil, et ton « carré vert » de contribution restera vide — or c'est exactement ce que regardent les recruteurs.

### 2.3 Installer les extensions VS Code (5 minutes)
```bash
code --install-extension ms-python.python          # support Python
code --install-extension ms-python.vscode-pylance  # autocomplétion, détection d'erreurs
code --install-extension ms-toolsai.jupyter        # exécuter les .ipynb dans VS Code
code --install-extension charliermarsh.ruff        # qualité et style de code
code --install-extension eamodio.gitlens           # historique Git, qui a écrit quoi
```
Si la commande `code` n'est pas reconnue : dans VS Code, `Ctrl+Shift+P` → **« Shell Command: Install 'code' command in PATH »**.

**Réglages recommandés** — copie ceci dans `.vscode/settings.json` à la racine de ton projet (le fichier `vscode_settings_modele.json` fourni dans ce dossier contient exactement ce contenu) :
```json
{
  "python.analysis.typeCheckingMode": "basic",
  "editor.rulers": [100],
  "editor.formatOnSave": true,
  "notebook.output.textLineLimit": 30,
  "files.autoSave": "afterDelay"
}
```

### 2.4 (Recommandé) Créer un environnement virtuel
Un « venv » = un espace isolé pour les bibliothèques de **ce** projet. Ça évite qu'une mise à jour casse tout, et c'est la norme professionnelle.
```bash
cd mon-projet
python -m venv .venv

# Activation :
# Windows (PowerShell) :  .venv\Scripts\Activate.ps1
# Windows (cmd)        :  .venv\Scripts\activate.bat
# macOS / Linux        :  source .venv/bin/activate

python -m pip install --upgrade pip
```
⚠️ Si PowerShell bloque l'activation : `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` (une seule fois).

---

## 3. Les comptes à créer (gratuits, 15 minutes)

| Service | Pourquoi | Quand |
|---|---|---|
| **Google Colab** (colab.research.google.com) | coder sans rien installer, GPU gratuit pour le deep learning | **avant la semaine 1** |
| **Kaggle** | datasets réels, cours courts, notebooks publics | avant la semaine 7 (le dataset de ton projet) |
| **Hugging Face** | modèles pré-entraînés, cours NLP gratuit, hébergement de démos (Spaces) | avant la semaine 38 |
| Anthropic / OpenAI / Mistral *(optionnel payant)* | API LLM pour le RAG (semaines 42-46) | semaine 42 — ou utilise **Ollama** en local, gratuit |
| Render / Railway *(optionnel)* | héberger ton API publiquement | semaine 49 |

Connecte bien **Colab et Kaggle avec le même compte Google** utilisé pour GitHub : tu gagneras du temps plus tard.

---

## 4. Prérequis semaine par semaine (le tableau à garder sous les yeux)

> **Colonne « À préparer d'avance »** = ce qu'il faut télécharger ou créer **avant** de commencer le bloc. C'est fait exprès : au Burkina, mieux vaut télécharger une grosse dépendance un jour où la connexion est bonne que rester bloqué trois jours en pleine semaine d'apprentissage.

| Semaines | Ce que tu fais | À installer (`pip install …`) | À préparer d'avance |
|---|---|---|---|
| **1** | méthode, comptes, carnet, projet fil rouge | *rien* | compte Colab, dépôt `ia-parcours` créé et poussé |
| **2-4** | Python : bases, structures, fichiers, classes, Git | *rien* (Python pur) | — |
| **5-6** | NumPy, vectorisation, normalisation | `numpy matplotlib` | — |
| **7-8** | Pandas, exploration, graphiques | `pandas openpyxl seaborn` | **télécharger le dataset de ton projet fil rouge** |
| **9-13** | maths : vecteurs, gradient, probabilités (appliquées) | *(déjà installés)* | — |
| **14-19** | workflow ML, évaluation, modèles simples | `scikit-learn joblib` | dataset crédit/churn (Kaggle) téléchargé |
| **20-26** | ensembles, SHAP, **projet ML complet** | `lightgbm xgboost shap pytest` | données du projet dans `data/raw/` |
| **27-31** | PyTorch, boucle d'entraînement | `torch` (version CPU suffit) | décider : entraînement en local ou sur Colab |
| **32-34** | CNN, transfer learning, démo | `torchvision streamlit` | dataset d'images (ex. PlantVillage) |
| **35-39** | séquences, Transformers, fine-tuning | `transformers datasets sentence-transformers accelerate` | compte Hugging Face + jeton d'accès |
| **40-41** | LLM, prompt engineering | *(rien de plus)* | décider API distante ou **Ollama** local |
| **42-44** | **RAG** (projet vitrine) | `faiss-cpu streamlit` | tes documents (PDF) à indexer |
| **45-46** | agents, function calling | `pydantic requests` (+ `openai` ou Ollama) | *optionnel* : clé API créditée de 5-10 € |
| **47-48** | MLOps, MLflow, tests, CI | `mlflow pytest evidently` | — |
| **49-50** | FastAPI, Docker, déploiement | `fastapi "uvicorn[standard]"` + **Docker Desktop** | compte Render ou Hugging Face Spaces |
| **51-52** | carrière : CV, LinkedIn, entretiens | *rien* | — |

**Règle d'or :** n'installe que ce dont tu as besoin **maintenant**. Installer PyTorch à la semaine 3 alors que tu apprends les variables Python, c'est 2 Go de téléchargement pour rien — et une source de découragement.

**Exception :** si ta connexion est irrégulière, télécharge **les 4 fichiers de dépendances fournis dans ce dossier** au moment où tu as du réseau, puis installe hors ligne. Commande unique :
```bash
pip install -r requirements_fondations.txt      # phases 1-2 (semaines 1-26)
pip install -r requirements_ml.txt             # fin du T2 (semaines 20-26)
pip install -r requirements_deep_learning.txt  # phases 3 (semaines 27-39)
pip install -r requirements_llm_deploiement.txt # phases 4 (semaines 40-50)
```

---

## 5. Travailler avec une connexion irrégulière (contexte Burkina)

C'est un facteur qui décide de la réussite du parcours. Six habitudes :

1. **Fais tes grosses installations le matin tôt ou la nuit**, quand le débit est meilleur.
2. **Télécharge les vidéos et datasets à l'avance** (une semaine de travail hors ligne).
3. **Le cours est en Markdown** — exprès : il s'ouvre dans VS Code sans connexion, tu as tout sur disque.
4. **Colab pour le deep learning**, VS Code en local pour Python/ML classique (léger, marche hors ligne).
5. **Sauvegarde ton travail sur GitHub à chaque fin de séance** (`git push`). Statistiquement, c'est ta protection contre une panne de machine.
6. **Garde une copie sur clé USB** des 2 projets finis. Rien n'est plus douloureux que perdre un projet.

> 💡 **Astuce Colab :** monte ton Google Drive pour sauvegarder tes notebooks automatiquement. Tu retrouveras ton travail depuis n'importe quel appareil.

---

## 6. Vérifier que tout est prêt (script fourni)

Dans ce dossier, lance :
```bash
python verifier_environnement.py
```
Il te dit **exactement** ce qui manque, étape par étape, avec les commandes à copier. Exemple de sortie en cours de parcours :
```
4. T2 · Machine Learning (semaines 14-26)
  ✓ sklearn   1.3.2   [requis]
  ✗ lightgbm  absent  [requis]
  → pip install lightgbm
```
Relance-le **au début de chaque phase** : tu sauras en 5 secondes si ton environnement suit.

---

## 7. Les 8 commandes Git à connaître par cœur

C'est 90 % de ton usage quotidien. Tu les taperas des milliers de fois.

```bash
# 1. Créer et publier un dépôt (une seule fois par projet)
git init
git branch -M main
git remote add origin https://github.com/TON-PSEUDO/mon-projet.git

# 2. Le cycle quotidien (à répéter à chaque fin de séance)
git status                       # qu'est-ce qui a changé ?
git add .                        # tout préparer
git commit -m "feat: ajoute le chargement des données"
git push                         # envoyer sur GitHub

# 3. Récupérer / inspecter
git log --oneline -5             # les 5 derniers commits
git diff                         # ce que j'ai modifié depuis le dernier commit
```

**Messages de commit utiles** (le recruteur lit l'historique : donne-lui envie) :
| À éviter | À écrire |
|---|---|
| `update` | `feat: ajoute la normalisation des variables` |
| `fix bug` | `fix: corrige le calcul du MAE sur les valeurs manquantes` |
| `test` | `docs: complète le README avec les résultats mesurés` |

⚠️ **Deux réflexes de survie :**
1. **Ne mets jamais une clé d'API dans ton code.** Elle part sur GitHub en 2 secondes et des robots la trouvent. Utilise une variable d'environnement + un fichier `.env` listé dans `.gitignore`.
2. **Un fichier `.gitignore` dans chaque projet** (les modèles de projets du pack en contiennent déjà un).

---

## 8. Ta checklist de démarrage (à cocher)

- [ ] `python --version` ≥ 3.10
- [ ] `git config --global user.name` et `user.email` renseignés (avec l'email GitHub)
- [ ] Les 5 extensions VS Code installées
- [ ] `vscode_settings_modele.json` copié dans ton projet en `.vscode/settings.json`
- [ ] Compte **Google Colab** créé
- [ ] Compte **Kaggle** créé
- [ ] Dépôt **`ia-parcours`** créé sur GitHub avec un README de 10 lignes
- [ ] `carnet.md` créé (Notions du jour / Erreurs du jour / Idée de projet)
- [ ] `python verifier_environnement.py` lancé → uniquement des ✓ pour la **phase 1**
- [ ] Semaine 1 cochée dans `plan_etude.html`

Quand les 10 cases sont cochées, tu es dans les meilleures conditions possibles. **Tu peux commencer.**

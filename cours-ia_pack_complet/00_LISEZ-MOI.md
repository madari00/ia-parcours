# 🎓 PACK « DEVENIR PRO DE L'IA » — Guide d'utilisation

**Pour qui :** toi, titulaire d'une **licence en technologie de génie informatique**, basé à Ouagadougou, qui veut se spécialiser en IA et décrocher un emploi dans le monde francophone occidental (France, Belgique, Suisse, Québec/Canada).

**Rythme prévu :** 5 à 10 h/semaine → **12 mois** pour être « employable ». *Ce n'est pas une promesse magique : c'est un plan réaliste, à condition de faire les exercices.*

---

## 1. Ce que contient le pack

| Fichier | Contenu | Tu l'utilises quand ? |
|---|---|---|
| `01_Partie1_Fondations.md` | Python + NumPy/Pandas + maths pour l'IA | Mois 1 à 3 |
| `02_Partie2_Machine_Learning.md` | Le ML classique (le cœur du métier) | Mois 3 à 6 |
| `03_Partie3_Deep_Learning.md` | Réseaux de neurones, CNN, transformers | Mois 6 à 9 |
| `04_Partie4_LLM_et_Deploiement.md` | LLM, RAG, agents, MLOps, Docker, API | Mois 9 à 12 |
| `05_Roadmap_52_semaines.md` | Le planning semaine par semaine + jalons | **Tous les lundis** |
| `06_Carriere_Occident_Francophone.md` | Marché, salaires réels, visa, CV, entretiens | Mois 4 puis mois 10-12 |
| `07_Annexes.md` | Glossaire FR/EN, antisèche, pièges, ressources | En permanence |
| `plan_etude.html` | **Tableau de bord interactif : 52 semaines à cocher**, jalons, ressources | Chaque lundi matin |
| **`SETUP/`** ⭐ | **Prérequis semaine par semaine**, script de diagnostic d'environnement, dépendances par phase, dépôt `ia-parcours` prêt à pousser | **Maintenant (10 min)** |
| `notebooks/*.ipynb` | 6 notebooks d'exercices (à compléter par toi) | À chaque chapitre |
| `notebooks/README_notebooks.md` | Mode d'emploi des notebooks | Une fois |
| `projets/projet_final/` | Projet de portfolio type (crédit/microfinance) : API + Streamlit + Docker + tests | Mois 10 à 12 |
| **`projets/projet_prix_cereales/`** ⭐ | **Projet vitrine sur données RÉELLES** (WFP, 2016-2026) : prévision des prix céréaliers + alerte précoce, API FastAPI, 9 tests | Immédiatement consultable |
| **`CV_Candidature/`** | **Ton CV 1 page (.docx éditable)** + guide de candidature | Mois 10-12, mais jette un œil maintenant |
| **`Entretiens/`** | **Simulation d'entretien complète** : 13 questions techniques, test chronométré, 7 questions RH pièges, grille de notation | Mois 8 puis mois 12 |

**Résultats mesurés (pas inventés) :**
- *Projet crédit* : régression logistique ROC-AUC **0,715** contre baseline métier 0,524.
- *Projet céréales* : baseline naïve **meilleure à 1-3 mois**, modèle ML **+10 % à 12 mois** ; alerte précoce PR-AUC **0,266** contre un taux de base de 0,114 (**2,3× le hasard**).
- Les deux pipelines tournent de bout en bout et les tests passent (`pytest -q`).

---

## 2. Comment lire ce cours (règle d'or : 30 / 70)

> **30 % du temps à lire, 70 % du temps à coder.**

Chaque chapitre suit toujours la même structure :

1. **🎯 Objectif** — ce que tu sauras faire après.
2. **💡 L'essentiel en 5 minutes** — l'intuition, avec une analogie simple.
3. **📘 Le cours** — la partie riche, chaque formule décodée symbole par symbole.
4. **💻 Le code** — version minimale, commentée, à retaper **toi-même** (ne pas copier-coller).
5. **⚠️ Les 3 erreurs classiques** — celles qui font échouer les débutants.
6. **✅ Quiz** — 5 questions, réponses à la fin du chapitre.
7. **🛠️ Exercices** — à faire avant de passer au chapitre suivant.

Si tu ne sais pas faire un exercice, ce n'est pas grave : relis la section du cours concernée, puis refais-le. **C'est exactement ça, le métier.**

---

## 3. Ton matériel (et comment te débrouiller avec peu)

| Besoin | Solution gratuite recommandée |
|---|---|
| Coder | **Google Colab** (colab.research.google.com) — rien à installer, GPU gratuit limité, marche sur connexion moyenne |
| Éditeur local (optionnel) | **VS Code** + Python 3 |
| Stockage du code | **GitHub** (obligatoire : c'est ton CV de demain) |
| Base de données d'apprentissage | Kaggle Datasets, UCI ML Repository, data.gouv.fr |
| Anglais technique | YouTube (chaînes de ML en anglais), docs officielles |

**Astuce connexion lente :** télécharge les vidéos et datasets aux heures creuses ; travaille beaucoup en mode « lecture + notes + code » plutôt qu'en streaming massif. Colab permet d'écrire et d'exécuter sans rien télécharger.

---

## 4. Les 6 vérités à accepter avant de commencer

1. **Ton diplôme (bac+3) ne suffit pas à lui seul** pour l'Occident : il te faut un **portfolio + des preuves de compétences**. La bonne nouvelle : en IA, les projets comptent autant (souvent plus) que le diplôme.
2. **Un an à 7 h/semaine = ~360 heures.** C'est le prix réel pour passer de « je sais coder un peu » à « je peux être embauché comme junior en data/IA ». Si tu peux faire 15 h/semaine, tu réduis à ~6 mois.
3. **Tu ne peux pas « être au niveau » des diplômés occidentaux en 3 mois.** Mais tu peux avoir **un profil complémentaire très recherché** : IA appliquée, LLM/RAG, déploiement, + ta capacité à travailler avec peu de ressources (très valorisée en Afrique et dans les boîtes qui y opèrent).
4. **L'anglais technique n'est pas négociable.** Pas besoin d'être bilingue : il faut pouvoir lire une doc, écrire un README, tenir une réunion de 20 min.
5. **Le visa est un problème séparé de la compétence.** Deux chemins dominent pour la France : (a) **master en France** (puis passeport talent + accès au marché), (b) **emploi à distance** d'abord. Détails dans `06_Carriere...`.
6. **La régularité bat l'intensité.** 1 h/jour > 8 h le samedi. Vraiment.

---

## 5. Ton premier pas, maintenant (30 minutes)

Tu as déjà **VS Code**, **Python** et **GitHub** → tu sautes la moitié des étapes.

1. Lis **`SETUP/00_Prerequis_et_environnement.md`, section 2** et fais les 3 réglages (10 min : version Python, identité Git, extensions VS Code).
2. Lance **`python SETUP/verifier_environnement.py`** : il te dit précisément ce qui manque pour la phase 1.
3. Copie le dossier **`SETUP/modele_depot_ia-parcours/`** quelque part sur ta machine, renomme-le `ia-parcours`, puis `git init` + `git push` vers ton dépôt GitHub (les commandes exactes sont dans la section 7 du même document).
4. Ouvre le notebook `notebooks/01_premiers_pas_python.ipynb` et fais les 3 premiers blocs.
5. Ouvre **`plan_etude.html`** et coche la **semaine 1**.
6. Note ta date de démarrage : `____ / ____ / 2026`. Ta « ligne d'arrivée employable » = cette date + ~13 mois.

---

> 💬 *« Le meilleur moment pour planter un arbre, c'était il y a 20 ans. Le second meilleur moment, c'est maintenant. »*
> Commence par la semaine 1. Bon courage — c'est un marathon, pas un sprint.

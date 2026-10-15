# 🗺️ PLAN DE ROUTE — 52 SEMAINES (5-10 h/semaine)

> **Profil de départ :** licence en technologie de génie informatique, bases de programmation, maths rouillées, 5-10 h/semaine.
> **Objectif à 12 mois :** profil **« junior IA appliquée »** crédible sur le marché francophone occidental (France, Belgique, Suisse, Québec), avec portfolio, spécialité RAG/LLM et un plan carrière clair.
> **Règle d'or :** on ne saute pas d'étape, mais **on ne reste jamais bloqué plus d'une semaine** sur un sujet. 85 % de maîtrise, puis on avance.

---

## 📊 Vue d'ensemble en 4 trimestres

| Trimestre | Semaines | Phase | Résultat concret |
|---|---|---|---|
| **T1** | 1-13 | Fondations | Python solide + NumPy/Pandas + maths IA + 3 notebooks sur GitHub |
| **T2** | 14-26 | Machine Learning | 2 projets ML complets + capacité à réussir un test technique junior |
| **T3** | 27-39 | Deep Learning | CNN + Transformers + fine-tuning HF + 1 projet vision ou NLP |
| **T4** | 40-52 | LLM, RAG, MLOps, Carrière | Application RAG déployée + API Docker + CV/LinkedIn + candidatures |

**Temps total estimé : 350 à 500 heures.**

---

# 🔹 TRIMESTRE 1 — FONDATIONS (semaines 1-13)

### Semaine 1 — Démarrage et méthode
- Lire le chapitre 0 (méthode) et le LISEZ-MOI.
- Créer : GitHub, Colab, carnet de notes (`carnet.md`).
- Choisir **ton projet fil rouge** (écris-le dans `cadrage_projet.md`).
- **Livrable :** dépôt `ia-parcours` créé avec un README de 10 lignes.

### Semaine 2 — Python : bases
- Chapitres 1.1 à 1.4. Variables, conditions, boucles, fonctions.
- Exercices 1 à 3 du chapitre 1 (convertisseur FCFA/€, analyse de texte).
- **Livrable :** 3 programmes Python poussés sur GitHub + premier `git commit` propre.

### Semaine 3 — Python : structures et fichiers
- Chapitres 1.5 à 1.7. Listes, dictionnaires, comprehensions, fichiers, erreurs.
- Exercice 3 (lecture de fichier + JSON) et exercice 4 (git).
- **Livrable :** un script qui lit un fichier de données et écrit un rapport JSON.

### Semaine 4 — Python : classes, modules + Git sérieux
- Chapitres 1.8 et 1.9. Classes, `import`, branches Git, Pull Request.
- Mini-projet : classe `GestionNotes` (ajouter, moyenne, top 3, export JSON).
- **Livrable :** **jalon T1-A** — un mini-projet Python propre et documenté.

### Semaines 5-6 — NumPy
- Chapitre 2 en entier + tous les exercices.
- Objectif : ne plus jamais écrire une boucle là où `X @ w` suffit.
- **Livrables :** `notebooks/01_numpy.ipynb` + exercice de normalisation.

### Semaines 7-8 — Pandas
- Chapitre 3 en entier + exercices.
- Choisir le **dataset réel de ton projet fil rouge** (Kaggle, data.gouv.fr, open.africa, HDX).
- **Livrable :** `notebooks/02_exploration.ipynb` — 3 graphiques + 5 observations écrites en français.

### Semaines 9-10 — Maths 1 et 2 (vecteurs, dérivées, gradient)
- Chapitres 4 et 5. C'est le moment le plus dur du parcours : **ne t'inquiète pas si ça rame.**
- Objectif : faire tourner le code de descente de gradient du chapitre 5 et voir la droite se rapprocher de la vraie.
- **Livrable :** `notebooks/03_premier_apprentissage.ipynb`.

### Semaines 11-12 — Maths 3 (probabilités, statistiques)
- Chapitre 6 + exercices. Simulation du test médical, biais/variance.
- **Livrable :** `notebooks/04_probas.ipynb` + une note de 1 page « ce que j'ai compris des probabilités ».

### Semaine 13 — Consolidation et rattrapage
- Refais les exercices non terminés. Relis ton carnet.
- Écris un **journal de progression** (une page : ce que je sais faire, ce qui bloque).
- **🏁 JALON T1 :** tu écris du Python sans aide, tu manipules des données, tu expliques gradient et probabilité. 3 notebooks publics sur GitHub.

---

# 🔹 TRIMESTRE 2 — MACHINE LEARNING (semaines 14-26)

### Semaines 14-15 — Cadrage et workflow
- Chapitres 7 et 8. Checklist de cadrage, pipelines, data leakage.
- **Livrable :** `cadrage_projet.md` complet pour ton projet fil rouge.

### Semaines 16-17 — Évaluation honnête
- Chapitre 9 + exercices (matrice de confusion, seuils, courbes ROC).
- Dataset à utiliser : **Credit Card Fraud** ou churn client.
- **Livrable :** `notebooks/05_metriques.ipynb` avec le seuil optimal **justifié en langage business**.

### Semaines 18-19 — Modèles simples
- Chapitre 10. Logistique, kNN, arbre. Comparaison en CV 5-folds.
- **Livrable :** tableau comparatif + arbre visualisé et transcrit en règles « si… alors… ».

### Semaines 20-21 — Ensembles (RF, XGBoost, LightGBM)
- Chapitre 11 + exercices. Early stopping, learning rate.
- **Livrable :** modèle principal du projet fil rouge (le meilleur des 2 trimestres).

### Semaines 22-23 — Non supervisé
- Chapitre 12. Segmentation + anomalies sur un dataset réel.
- **Livrable :** `notebooks/06_segmentation.ipynb` avec segments **nommés en français** et actions proposées.

### Semaines 24-26 — PROJET ML COMPLET ⭐
- Chapitre 13 + projet final. README professionnel, SHAP, rapport d'une page.
- **Livrable :** dépôt `projet-ml-<ton-sujet>` avec modèle `.pkl`, tests, figures, limites.
- **🏁 JALON T2 :** tu peux passer un test technique junior (Python + ML + métriques) et le justifier. **C'est le seuil d'employabilité minimal.** Si tu t'arrêtes ici, tu peux déjà postuler à des postes de **data analyst / junior data scientist** (avec un peu d'anglais).

### Semaine 26 (bis) — Bilan mi-parcours
- Relis `06_Carriere_Occident_Francophone.md` sections 1-5.
- Crée ton **profil LinkedIn** (en français) avec les 2 projets. **Les recruteurs passent là d'abord.**
- **Question à te poser honnêtement :** est-ce que je vise l'emploi direct, le master, ou le freelance distant ? (cf. section 6 du guide carrière)

---

# 🔹 TRIMESTRE 3 — DEEP LEARNING (semaines 27-39)

### Semaines 27-28 — Neurones et réseaux
- Chapitres 14 et 15. Écris ta première boucle PyTorch **de mémoire** à la fin.
- **Livrable :** `notebooks/07_mlp_pytorch.ipynb` (problème `make_moons`, puis ton dataset tabulaire).

### Semaine 29 — Comparaison DL vs ML sur tabulaire
- Entraîne un MLP sur ton projet fil rouge, compare à LightGBM.
- **Livrable :** 1 page de conclusion (c'est une réponse d'entretien toute prête).

### Semaines 30-32 — Vision (CNN)
- Chapitre 16. Fashion-MNIST (≥ 90 %), puis **transfer learning** ResNet18 sur un dataset de plantes ou d'images de ton domaine.
- **Livrable :** `notebooks/08_cnn.ipynb` + démo d'inférence sur **tes propres photos**.

### Semaines 33-34 — Transfer learning + augmentation
- Exercice d'ablation (avec/sans augmentation, avec/sans dropout). Déploie la démo sur Hugging Face Spaces.
- **Livrable :** lien public dans ton README.

### Semaines 35-37 — Séquences et Transformers
- Chapitres 17 et 18. LSTM sur une série (énergie, météo, prix) + embeddings de phrases.
- **Livrable :** `notebooks/09_sequences.ipynb` + schéma d'un bloc Transformer dessiné par toi (à mettre dans ton portfolio : ça impressionne).

### Semaines 38-39 — Hugging Face et fine-tuning
- Chapitre 19. Fine-tuning d'un modèle multilingue sur un dataset français.
- **Livrable :** `notebooks/10_finetuning.ipynb` avec accuracy avant/après + carte du modèle.
- **🏁 JALON T3 :** tu sais entraîner et adapter un réseau de neurones. Tu peux viser des postes « ML engineer junior » et « computer vision junior ».

---

# 🔹 TRIMESTRE 4 — LLM, RAG, DÉPLOIEMENT, CARRIÈRE (semaines 40-52)

### Semaines 40-41 — LLM et prompt engineering
- Chapitres 20 et 21. Écris 5 prompts professionnels, construis un jeu d'évaluation de 20 cas.
- **Livrable :** `prompts/` dans ton dépôt + rapport d'évaluation.

### Semaines 42-44 — RAG (ton projet vitrine) ⭐
- Chapitre 22. Construis un RAG sur des documents réels (santé, agriculture, droit, ONG).
- Ajoute : citations, recherche hybride, re-ranking, évaluation sur 30 questions.
- **Livrable :** dépôt `rag-<domaine>` avec README + démo + tableau de résultats.

### Semaines 45-46 — Agents
- Chapitre 23. Un agent à 2-3 outils avec garde-fous et journalisation.
- **Livrable :** dépôt `agent-<domaine>`.

### Semaines 47-48 — MLOps
- Chapitre 24. MLflow sur ton projet, 3 tests pytest, CI GitHub Actions, rapport de dérive.
- **Livrable :** badges CI dans le README (détail qui marque).

### Semaines 49-50 — Déploiement
- Chapitre 25. API FastAPI + pydantic + Docker + déploiement Render/HF Spaces.
- **Livrable :** **URL publique fonctionnelle** — le critère n°1 que regardent les recruteurs.
- **🏁 JALON T4 :** tu as un portfolio de 4-5 projets dont 1 application déployée.

### Semaines 51-52 — Carrière : passer à l'action
- Chapitre 26 (éthique, RGPD) pour l'entretien.
- Rédiger : CV (1 page, format occidental), LinkedIn, portfolio (GitHub Pages ou Notion), pitch de 2 minutes.
- Lancer **20 candidatures/ciblages** + 10 messages de réseautage. Préparer les 15 questions d'entretien du guide carrière.
- **🏁 JALON FINAL :** tu es un candidat junior **crédible** avec preuves, pas un postulant sans portfolio.

---

## ✅ Jalons de contrôle (à ne pas négliger)

| Jalon | Question de validation | Si NON |
|---|---|---|
| Fin S13 | Est-ce que je code sans tutoriel ? | refaire les exercices 1-6, +2 semaines |
| Fin S26 | Puis-je expliquer une matrice de confusion et un data leakage ? | relire les chapitres 8-9 |
| Fin S39 | Puis-je écrire une boucle d'entraînement PyTorch et adapter un modèle HF ? | refaire chapitres 15 et 19 |
| Fin S50 | Ai-je une URL publique et un README propre ? | consacrer 2 semaines au déploiement |
| Fin S52 | Ai-je envoyé ≥ 50 candidatures bien ciblées ? | c'est un problème de volume, pas de compétence |

## 📈 Signaux que tu progresses vraiment
- Tu lis le code des autres sur GitHub sans être perdu.
- Tu écris dans ton carnet des **erreurs** plus que des notions (c'est bon signe).
- Tu commences à avoir des avis (« pour ce problème, je prendrais LightGBM »), justifiés.
- Tu expliques à quelqu'un d'autre un concept d'IA avec une analogie simple.
- ⚠️ **Signal d'alerte :** tu passes plus de temps à regarder des vidéos qu'à coder → applique immédiatement la règle 30/70.

## 🌍 Adapter le rythme à la réalité du Burkina
- **Coupures d'électricité / internet :** télécharge les datasets et vidéos **à l'avance**, garde une semaine de travail hors ligne (cours en Markdown + Colab ouvert). Ce pack est en Markdown exprès.
- **Colab gratuit :** limite d'usage GPU. Utilise-le pour le deep learning uniquement ; fais le ML classique en CPU.
- **Période de fortes pluies (juillet-septembre) :** planifie des semaines plus légères ; anticipe en avance sur le trimestre 3.
- **Coût :** tout le parcours est faisable à 0 € si tu restes sur Colab + Hugging Face Spaces. Les seuls euros utiles : ~10-20 €/mois de crédits API LLM au trimestre 4 (ou 0 € avec Ollama en local).

---

## 🗓️ Modèle de semaine type (à recopier dans ton carnet)

| Jour | Bloc | Durée | Contenu |
|---|---|---|---|
| Lundi | Lecture | 1 h | Chapitre(s) de la semaine + notes |
| Mardi | Code | 1 h | Retaper les exemples sans regarder |
| Mercredi | Exercices | 1 h | Exercices du chapitre |
| Jeudi | Projet | 1 h | Appliquer au projet fil rouge |
| Vendredi | Révision | 0,5 h | Quiz + carnet + révision espacée |
| Samedi | Bloc profond | 2 h | Nouveau sujet / défi / Kaggle |
| Dimanche | Veille | 0,5 h | 1 article ou 1 vidéo technique |

**Total : 7 h.** Si tu n'as que 5 h : garde lundi, mercredi, vendredi, samedi. Si tu as 10 h : ajoute 1 h les mardi/jeudi et 1 h supplémentaire le samedi.

---

## 🏁 Après les 52 semaines : 3 trajectoires possibles

1. **Emploi en France/Belgique/Suisse** → il te faudra très probablement un **master** (voir guide carrière, section 5). Ce parcours te rend crédible pour les admissions et te donne un avantage énorme en entretien. Recandidature possible dès février-mars pour la rentrée de septembre.
2. **Télétravail depuis le Burkina** → cible les PME/startups francophones, ONG, agences; facture 15-35 €/h en junior. Ce parcours te suffit techniquement.
3. **Québec** → très ouvert aux francophones, mais le diplôme local ou l'expérience québécoise compte beaucoup. Combine avec un DESS/master ou une arrivée via un employeur.

**Dans tous les cas : continue.** Le marché IA évolue vite ; tes 52 semaines sont une base, pas un aboutissement. Le vrai avantage compétitif : ne jamais arrêter d'apprendre.

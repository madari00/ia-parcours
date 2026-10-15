# 📎 ANNEXES — Glossaire, antisèche, pièges, ressources

---

## A. Glossaire français ↔ anglais (indispensable en entretien)

| Français | Anglais | Sens |
|---|---|---|
| Intelligence artificielle | Artificial Intelligence (AI) | ensemble des techniques |
| Apprentissage automatique | Machine Learning (ML) | apprendre à partir de données |
| Apprentissage profond | Deep Learning (DL) | réseaux de neurones profonds |
| Apprentissage supervisé | Supervised learning | avec étiquettes |
| Apprentissage non supervisé | Unsupervised learning | sans étiquettes |
| Apprentissage par renforcement | Reinforcement learning | par récompenses |
| Caractéristique | Feature | variable d'entrée |
| Cible / étiquette | Target / Label | ce qu'on prédit |
| Jeu d'entraînement | Training set | pour apprendre |
| Jeu de validation | Validation set | pour régler |
| Jeu de test | Test set | pour juger une fois |
| Surapprentissage | Overfitting | apprend le bruit |
| Sous-apprentissage | Underfitting | trop simple |
| Régularisation | Regularization | pénaliser la complexité |
| Fonction de coût | Loss / cost function | l'erreur à minimiser |
| Descente de gradient | Gradient descent | l'algorithme d'apprentissage |
| Taux d'apprentissage | Learning rate | taille du pas |
| Rétropropagation | Backpropagation | calcul des gradients |
| Taux de vrais/faux positifs | True/False Positive Rate | matrice de confusion |
| Précision | Precision | alertes justes |
| Rappel / sensibilité | Recall / sensitivity | cas détectés |
| Exactitude | Accuracy | % de bonnes réponses en tout |
| Valeurs manquantes | Missing values | trous dans les données |
| Valeur aberrante | Outlier | point extrême |
| Fuite de données | Data leakage | information du test dans le train |
| Dérive | Drift | le monde change, le modèle se décale |
| Ajustement des hyperparamètres | Hyperparameter tuning | réglages |
| Validation croisée | Cross-validation | évaluation robuste |
| Graine aléatoire | Random seed | reproductibilité |
| Encodeur | Encoder | partie qui comprend |
| Décodeur | Decoder | partie qui génère |
| Plongement / vecteur de sens | Embedding | mot → vecteur |
| Fenêtre de contexte | Context window | tokens lisibles |
| Génération augmentée par récupération | RAG | LLM + documents |
| Ajustement fin | Fine-tuning | spécialiser un modèle |
| Quantification | Quantization | réduire la précision des poids |
| Agent | Agent | LLM + outils |
| Appel de fonction | Function calling / tool use | le modèle choisit un outil |
| Chaîne d'entraînement | Pipeline | étapes automatisées |
| Mise en production | Deployment | rendre disponible |
| Surveillance | Monitoring | suivre la santé du modèle |
| Évaluation A/B | A/B testing | comparer deux versions |
| Fiche modèle | Model card | documentation du modèle |
| Modèle de langage de grande taille | Large Language Model (LLM) | GPT, Claude, Mistral… |

---

## B. Antisèche (à imprimer / garder sur ton bureau)

### B.1 Choisir la métrique
| Situation | Métrique principale | À regarder aussi |
|---|---|---|
| Classes équilibrées | Accuracy, F1 | matrice de confusion |
| Classes déséquilibrées | **Rappel, PR-AUC, F1** | précision, seuil retenu |
| Coût asymétrique des erreurs | F-beta adapté, coût moyen | courbe précision-rappel |
| Classement (scoring) | **ROC-AUC** | PR-AUC si < 5 % de positifs |
| Régression | **MAE** | RMSE, R², erreurs par segment |
| Séries temporelles | **MAE, MAPE** | comparaison à la persistance |
| Clustering | Silhouette | cohérence métier |
| RAG | Fidélité, rappel de recherche | taux de refus correct |

### B.2 Le workflow ML en 10 lignes (poster mental)
```
1. Cadrer le problème + baseline + coût des erreurs
2. Collecter et explorer (EDA) : distributions, manquants, doublons
3. Séparer train/val/test (stratifié ou temporel)
4. Construire un Pipeline (imputation, encodage, normalisation)
5. Commencer SIMPLE : logistique / arbre
6. Mesurer avec CV (5 folds) et la bonne métrique
7. Améliorer : features, puis Random Forest, puis boosting
8. Réglage (Random Search / Optuna) + early stopping
9. Interpréter (SHAP) + vérifier l'équité par sous-groupe
10. Évaluer UNE fois sur le test → déployer → surveiller la dérive
```

### B.3 Maths essentielles
| Notion | Formule | Sens |
|---|---|---|
| Norme | $\sqrt{\sum x_i^2}$ | longueur |
| Produit scalaire | $\sum x_i y_i$ | ressemblance |
| Similarité cosinus | $\frac{x\cdot y}{\|x\|\|y\|}$ | ressemblance indépendante de la taille |
| Sigmoid | $\frac{1}{1+e^{-x}}$ | vers [0,1] |
| Softmax | $\frac{e^{z_i}}{\sum_j e^{z_j}}$ | distribution de probabilités |
| ReLU | $\max(0,x)$ | non-linéarité standard |
| MSE | $\frac1n\sum(y-\hat y)^2$ | erreur régression |
| Entropie croisée | $-\sum y\log\hat y$ | erreur classification |
| Descente de gradient | $w \leftarrow w-\alpha\nabla L$ | apprendre |
| Précision | $\frac{VP}{VP+FP}$ | alertes justes |
| Rappel | $\frac{VP}{VP+FN}$ | cas détectés |
| F1 | $\frac{2PR}{P+R}$ | équilibre |
| Bayes | $P(A\mid B)=\frac{P(B\mid A)P(A)}{P(B)}$ | croyance mise à jour |
| Attention | $\text{softmax}(QK^T/\sqrt{d_k})V$ | pondération contextuelle |

### B.4 Traitement des urgences (dépannage express)
| Symptôme | Cause probable | Geste immédiat |
|---|---|---|
| `ModuleNotFoundError` | lib non installée / mauvais environnement | `pip install X` ; vérifie l'interpréteur |
| `Shape mismatch` | dimensions incompatibles | affiche `.shape` à chaque étape |
| `NaN` dans la loss | lr trop grand, log(0), division par 0 | lr ÷ 10, ajoute `1e-8` |
| Score test trop beau (> 0,99 AUC) | **fuite de données** | cherche une variable « contenant la réponse » |
| Modèle bon en local, mauvais en prod | distribution différente | compare les distributions (drift) |
| Mémoire saturée (Colab) | batch trop grand | batch ÷ 2, réduis le modèle, vide les variables |
| Entraînement très lent | pas de GPU / pas de vectorisation | Colab GPU, remplace les boucles par NumPy |
| Résultats non reproductibles | graines non fixées | `random_state=42`, `torch.manual_seed(42)` |
| API ne répond pas en ligne | hôte 0.0.0.0, port, pare-feu | `--host 0.0.0.0 --port 8000`, vérifie les logs |

---

## C. Les 12 pièges qui font échouer les débutants (et leurs solutions)

| # | Piège | Solution |
|---|---|---|
| 1 | Tutoriel-hopping | un seul cours à la fois, jusqu'au bout |
| 2 | Fuite de données | Pipelines, split d'abord, features temporelles par date |
| 3 | Métrique inadaptée | choisis la métrique **après** avoir chiffré le coût des erreurs |
| 4 | Overfitting ignoré | compare toujours train/validation, early stopping |
| 5 | Ne pas normaliser | StandardScaler avant kNN, SVM, k-means, réseaux |
| 6 | Classes déséquilibrées | rappel/PR-AUC, class_weight, seuil ajusté |
| 7 | Tout dans un notebook | code réutilisable dans `src/`, modèle sauvegardé |
| 8 | Pas de README | 60 secondes de lecture = la vitrine |
| 9 | Projet Titanic énième | choisis un problème réel de ton pays |
| 10 | Pas d'anglais | 30 min/jour de lecture technique en anglais |
| 11 | Travailler isolé | communauté, pair-review, Kaggle |
| 12 | Attendre d'être « prêt » | postule au jalon 2, apprends en marchant |

---

## D. Ressources gratuites classées (par ordre d'utilité pour ton parcours)

**Cours et livres**
- **Cours de ce pack** → à terminer d'abord. Ne disperse pas ton énergie.
- **Kaggle Learn** (gratuit, court, pratique) : Python, Pandas, Intro to ML, Feature Engineering, Intro to Deep Learning.
- **Machine Learning Specialization** (Andrew Ng, Coursera — accès auditable gratuit) : la meilleure pédagogie pour les fondations ML.
- **Deep Learning Specialization** (Andrew Ng) ou **fast.ai** (pédagogique et pratique, en anglais).
- **Andrej Karpathy — « Neural Networks: Zero to Hero »** (YouTube) : la meilleure ressource pour *comprendre vraiment* les réseaux et les LLM.
- **Hugging Face NLP Course** (gratuit, en français disponible pour plusieurs chapitres) : la référence pratique LLM.
- **StatQuest** (YouTube) : statistiques et ML expliqués très simplement.

**Références à garder ouvertes**
- Documentation **scikit-learn** (ils ont un « user guide » remarquable), **Pandas**, **PyTorch**, **transformers**, **FastAPI**.
- *Hands-On Machine Learning* (Aurélien Géron, O'Reilly) : le meilleur livre pratique ML+DL. La version anglaise récente est la meilleure ressource unique.
- *Designing Machine Learning Systems* (Chip Huyen) : la référence MLOps/production.
- *Dive into Deep Learning* (d2l.ai) : gratuit, interactif, en plusieurs langues.

**Pratique**
- **Kaggle** : compétitions, datasets, notebooks publics — c'est ton terrain d'entraînement.
- **Hugging Face** : modèles, datasets, Spaces (hébergement gratuit de démos).
- **DrivenData** : compétitions à impact social (santé, agriculture, humanitaire) — parfait pour ton portfolio.
- **Zindi** : compétitions de data science **africaines** — excellent pour se faire remarquer et travailler sur des problèmes locaux.

**Français / Afrique**
- **AUF** (Agence Universitaire de la Francophonie) : formations, bourses, réseaux.
- **Data science africaine** : communautés Zindi, AI Saturdays, Deep Learning Indaba, Masakhane (NLP africain), GhanaNLP.
- **Langues locales** : Masakhane, Lacuna Fund, projets open source de corpus — une niche où tu peux publier et te faire connaître **vite**.

**Communautés à rejoindre cette semaine**
- Discord/Slack francophones « Data Science FR », « MLOps FR », « Hugging Face FR ».
- Groupes LinkedIn : #DataScience, #IA, #LLM, communautés d'anciens étudiants burkinabè en France.
- Meetups (en ligne) de Paris/Bruxelles/Montréal : en ligne, tu peux y assister depuis Ouagadougou.

---

## E. Plan de secours : si tu perds la motivation

**Semaine difficile ?** Règle du **minimum vital** : 20 minutes de code par jour, même mauvais. Le but est de ne pas rompre la chaîne.

**Mois difficile ?** Refais un projet que tu as déjà terminé, en mieux (visualisations, README, tests). Sentir qu'on progresse vaut mieux que d'apprendre du neuf dans la douleur.

**Passage à vide complet ?** Change de format : écoute/aide quelqu'un d'autre (expliquer = apprendre × 2), refais le quiz du chapitre 9, ou nettoie et documente ton GitHub.

**Quand tu doutes du bien-fondé de l'effort, rappelle-toi :** chaque projet terminé est un actif concret qui te suit, contrairement à une vidéo regardée. Le diplôme ouvre la porte, le portfolio te fait entrer.

---

## F. Ce que tu devrais pouvoir faire à la fin (récapitulatif de sortie)

- [ ] Écrire du Python propre, structuré, testé.
- [ ] Manipuler des données avec Pandas/NumPy (+ SQL basique à intermédiaire).
- [ ] Mener un projet ML complet de bout en bout, avec une évaluation honnête.
- [ ] Entraîner et adapter un réseau de neurones (vision, texte).
- [ ] Construire un **RAG avec citations** et l'évaluer.
- [ ] Créer un **agent** simple avec garde-fous.
- [ ] Déployer une **API FastAPI dockerisée** avec URL publique.
- [ ] Parler de **drift, versioning, surveillance, RGPD, AI Act**.
- [ ] Expliquer tes choix techniques à un non-technicien, en **français** et en **anglais**.
- [ ] Présenter un **portfolio de 4 projets** et un CV d'une page.

**Si tu coches 8 cases sur 10 : tu es dans les 10 % des candidats juniors francophones. Continue.**

# 📄 CV — version à personnaliser (format France / Belgique / Suisse)

> ⚠️ **Tout ce qui est entre [CROCHETS] est à remplacer par TES informations.** Les chiffres des projets sont **réels** (mesurés dans ce pack) : tu peux les garder tels quels, ce sont tes preuves.

---

## Structure d'une page — à recopier dans Word / Google Docs

```
════════════════════════════════════════════════════════════════════════
                             [PRÉNOM NOM]
        Data Scientist / AI Engineer junior — Machine Learning & LLM/RAG

  Ouagadougou, Burkina Faso · [email] · [+226 XX XX XX XX]
  GitHub : github.com/[pseudo] · LinkedIn : linkedin.com/in/[profil]
  Démo en ligne : [URL de ton RAG ou de ton API déployée]
════════════════════════════════════════════════════════════════════════

PROFIL
Titulaire d'une licence en technologie de génie informatique, spécialisé en
machine learning appliqué et en IA générative (LLM, RAG). Auteur de projets
déployés sur des données réelles africaines, avec une pratique stricte de
l'évaluation honnête des modèles (baselines, validation temporelle, détection de
fuite de données). Autonome, orienté résultats mesurables. Recherche un poste
junior en data science / IA appliquée. Mobilité : [France / Belgique / Québec].

COMPÉTENCES TECHNIQUES
Langages           Python, SQL, Git/GitHub
Machine Learning   scikit-learn, LightGBM, XGBoost, séries temporelles,
                   validation croisée, métriques, SHAP
Deep Learning      PyTorch, CNN, Transformers, fine-tuning Hugging Face
IA générative      Prompt engineering, embeddings, RAG (FAISS), évaluation LLM,
                   agents et function calling
Données            pandas, NumPy, nettoyage, feature engineering, séries
                   temporelles, détection de fuite de données
Déploiement        FastAPI, pydantic, Streamlit, Docker, pytest, CI GitHub Actions
Langues            Français (natif), Anglais (technique, lecture/écriture pro)

PROJETS  ← la section que les recruteurs lisent en premier

Prévision des prix céréaliers — Burkina Faso (WFP, 22 656 observations réelles)
Python · LightGBM · pandas · FastAPI · Streamlit
• Construit un pipeline complet sur 10 ans de données publiques du Programme
  Alimentaire Mondial (64 marchés, 3 céréales) : nettoyage, variables temporelles,
  validation temporelle stricte.
• Mesuré les baselines naïves (persistance, saisonnier) : démontré que le modèle
  ML apporte +10 % de précision à 12 mois, et documenté honnêtement que la
  méthode naïve reste meilleure à 1-3 mois.
• Développé un classifieur d'alerte précoce : ROC-AUC 0,692 et PR-AUC 0,266
  contre un taux de base de 0,114 (2,3× le hasard), 60 % des flambées détectées.
• Détecté et corrigé une fuite de données (MAPE anormalement bas de 0,2 %) grâce
  à un test automatisé intégré à la CI.
• API FastAPI + interface Streamlit, 9 tests automatisés → [URL de démo]

Prédiction du risque de défaut de crédit — microfinance
Python · scikit-learn · FastAPI · Docker
• Modèle d'aide à la décision sur 6 020 dossiers, avec choix du seuil de décision
  fondé sur le coût réel des erreurs (faux négatifs privilégiés en priorité).
• ROC-AUC 0,715 contre 0,524 pour la règle métier existante ; régression logistique
  retenue sur la forêt aléatoire pour son explicabilité — performance **et**
  conformité (droit à l'explication, RGPD).
• Contrôle d'équité par ville : écart d'AUC identifié entre zones urbaines et
  rurales, commenté comme risque d'exclusion d'accès au crédit.
• API conteneurisée avec validation des entrées (pydantic) et tests d'intégration.

[PROJET RAG — à construire au mois 10 : « Chatbot documentaire »]
Python · FAISS · sentence-transformers · Streamlit
• Système de questions-réponses sur [XXX] documents de [domaine] avec citations
  des sources et droit de refus explicite (« je ne trouve pas »).
• Recherche hybride (lexicale + vectorielle) et re-ranking ; évalué sur 30 questions
  de référence : [XX] % de fidélité, [XX] % de refus corrects.
• Déployé → [URL]

FORMATION
2026  Licence en technologie de génie informatique — [Université], [Ville, Pays]
2026  Autoformation intensive en data science et IA appliquée (520 h) :
      machine learning, deep learning, LLM/RAG, MLOps — portfolio de projets
      déployés sur données réelles

[EXTRAS — si tu as de la place]
• Anglais technique · Lecture de documentation et publications scientifiques
• Contribution open source / compétitions : [Kaggle, Zindi — à remplir]
• Bénévolat / association : [optionnel, valorise le leadership]
```

---

## Les 8 règles à respecter (recruteurs France / Belgique / Québec)

| Règle | Pourquoi |
|---|---|
| **1 page maximum** | au-delà, le recruteur ne lit pas la fin |
| **Projets AVANT expérience** (profil junior) | tes projets sont tes preuves les plus récentes et les plus parlantes |
| **Chiffres et résultats, pas d'adjectifs** | « ROC-AUC 0,715 contre 0,524 » ≫ « excellent niveau en ML » |
| **Liens cliquables en en-tête** | GitHub + démo : le recruteur doit pouvoir vérifier en 1 clic |
| **Pas de barres de progression** (« Python : 80 % ») | ça ne veut rien dire et ça fait amateur |
| **Pas de photo en France** (optionnelle) | évite tout risque de discrimination ; au Québec, encore moins |
| **Aucune mention discriminante** | âge, situation familiale, nationalité : à retirer |
| **Mots-clés techniques explicites** | les CV sont souvent filtrés par mots-clés (ATS) : nomme les outils |

## Ce qui fait la différence pour un candidat étranger

1. **La spécialisation lisible** : « LLM / RAG » dans le titre plutôt que « passionné d'IA ». Les recruteurs cherchent une case à cocher.
2. **Une URL de démonstration** : le seul moyen de vérifier ta compétence à distance.
3. **La mention de mobilité** : « Mobilité France / disponible pour visa » rassure sur l'intention. ⚠️ N'écris **jamais** « besoin d'un visa » dans le CV — ça se discute en entretien.
4. **Une lettre de motivation de 6 lignes** (pas un roman) :
```
Madame, Monsieur,

Votre offre de [poste] chez [entreprise] correspond au profil que je construis
depuis un an : machine learning appliqué sur données réelles et IA générative.
Mon projet de prévision des prix céréaliers au Burkina Faso — 22 656 observations
du Programme Alimentaire Mondial, API déployée, 9 tests automatisés — m'a appris
à mesurer un modèle avant de le vanter : j'y documente les cas où une baseline
naïve bat mon modèle.
Je serais heureux de vous présenter ma démarche en entretien,
[Signature]
```
5. **Postuler en volume et de façon ciblée** : 1 candidature personnalisée vaut 10 candidatures génériques — mais il faut en envoyer 50+.

---

## À faire dès maintenant (30 minutes)

1. Crée ton CV sur **Google Docs** (gratuit, export PDF) à partir de la structure ci-dessus.
2. Remplace tous les `[CROCHETS]`.
3. Vérifie les 8 règles du tableau.
4. Exporte en **PDF** : nomme le fichier `CV_Prenom_Nom_DataScientist.pdf`.
5. Vérifie la lisibilité sur téléphone (la moitié des recruteurs lisent sur mobile).
6. Crée/actualise ton **LinkedIn** avec le même titre et le même contenu, puis publie ton premier projet.

> 💡 **Ne mens jamais sur un chiffre.** Les recruteurs techniques demandent à voir le notebook. Tes vrais chiffres — même modestes — construisent une crédibilité qui ne s'effondre pas en entretien.

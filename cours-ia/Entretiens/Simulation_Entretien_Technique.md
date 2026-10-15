# 🎤 SIMULATION D'ENTRETIEN — Data Scientist / AI Engineer junior

> **Comment utiliser ce document :** ne le lis pas comme un cours. Utilise-le comme une **salle d'entraînement**.
> Les réponses modèles sont là pour te montrer la *structure* attendue, pas pour être récitées mot à mot.

---

## 🔧 Mode d'emploi (3 modes, dans cet ordre)

| Mode | Comment | Durée |
|---|---|---|
| **1. Auto-évaluation écrite** | Lis la question, écris ta réponse, **puis** compare à la réponse modèle. Note ce qui manquait. | 2 × 1 h |
| **2. Oral seul, enregistré** | Réponds à voix haute en te filmant/enregistrant. Réécoute. C'est inconfortable et **extrêmement** efficace. | 3 × 30 min |
| **3. Simulation avec partenaire** | Quelqu'un te pose les questions, te coupe, te relance. Conditions réelles. | 1 h |

**Règle des 90 secondes :** une réponse technique = 60-90 secondes. Plus long = tu perds le recruteur. Structure : *définition courte → exemple concret → conséquence pratique*.

---

## 🎬 ÉTAPE 0 — Ton pitch de 2 minutes (à mémoriser)

C'est la première question de tout entretien : *« Parlez-moi de vous. »* Un mauvais pitch tue la suite.

> « Je suis titulaire d'une licence en technologie de génie informatique. Il y a un an, j'ai choisi de me spécialiser en machine learning appliqué et en IA générative, parce que c'est là que la demande est la plus forte et que je pouvais y apporter quelque chose de rare : la connaissance de terrains que les modèles comprennent mal.
>
> J'ai suivi une formation structurée de 520 heures — maths, machine learning, deep learning, LLM et déploiement — et je l'ai appliquée à deux projets sur données réelles.
>
> Le premier porte sur les prix céréaliers au Burkina Faso : 22 656 observations du Programme Alimentaire Mondial, 64 marchés. J'y ai construit un pipeline complet, comparé mes modèles aux baselines naïves, et j'y ai découvert une fuite de données que j'ai corrigée avec un test automatisé. Le résultat honnête : mon modèle apporte un gain à 12 mois, mais la méthode naïve reste meilleure à court terme — et je le documente au lieu de le cacher.
>
> Le second porte sur le risque de défaut de crédit en microfinance, avec la même exigence : ROC-AUC de 0,715 contre 0,524 pour la règle métier en place.
>
> Aujourd'hui je cherche un poste junior en data science ou IA appliquée, avec une préférence pour les projets où la rigueur méthodologique compte plus que l'effet d'annonce. »

**Pourquoi ce pitch fonctionne :** il dit qui tu es, ce qui te rend légitime, tes preuves chiffrées, et il se termine par une demande claire. **Aucune phrase creuse.**

---

## PARTIE A — 13 questions techniques (avec réponses modèles)

### A1. « Qu'est-ce qu'une fuite de données (*data leakage*) ? »
> « C'est quand une information que le modèle n'aurait pas au moment de la prédiction se retrouve dans les variables d'entraînement. Le score paraît excellent, mais le modèle est inutilisable en production.
>
> Mon exemple concret : sur mon projet de prévision des prix, ma première version affichait un MAPE de 0,2 % — impossible pour des prix alimentaires. J'avais inclus une variable construite avec le prix du mois courant, alors que la prévision se fait un mois avant. J'ai corrigé, et surtout j'ai écrit un **test automatisé** qui corrompt le prix du mois courant et vérifie qu'aucune variable ne change : il tourne à chaque entraînement.
>
> Les trois autres formes que je connais : normaliser ou imputer avant de séparer train et test ; utiliser une variable qui contient la réponse ; et sur des séries temporelles, tirer le découpage au hasard au lieu de couper par date. »

### A2. « Différence entre biais et variance ? »
> « Le biais, c'est l'erreur due à un modèle trop simple : il rate la structure des données, on parle de sous-apprentissage. La variance, c'est l'erreur due à un modèle trop sensible à l'échantillon : il apprend le bruit, on parle de surapprentissage.
>
> Diagnostic concret : je regarde l'écart entre le score d'entraînement et le score de validation. Un gros écart = variance. Deux scores mauvais et proches = biais.
>
> Les remèdes diffèrent : contre la variance, plus de données, régularisation, early stopping, modèle plus simple ; contre le biais, modèle plus expressif ou meilleures variables. »

### A3. « Votre dataset contient 2 % de positifs. Quelles métriques ? »
> « Surtout pas l'exactitude : un modèle qui répond "négatif" à chaque fois aurait 98 % d'exactitude et zéro utilité.
>
> Je regarde la **PR-AUC** et le **rappel** sur la classe minoritaire, et j'ajuste le seuil de décision selon le coût des erreurs. Côté entraînement : `class_weight="balanced"`, et si nécessaire du ré-échantillonnage — mais toujours **dans** le pipeline et après la séparation des données, sinon fuite.
>
> Sur mon projet d'alerte de flambée, le taux de base était de 11 % : j'ai comparé ma PR-AUC de 0,266 à ce taux de base, ce qui donne 2,3 fois mieux que le hasard. C'est cette comparaison qui rend le chiffre interprétable. »

### A4. « Quand préférez-vous le rappel, quand la précision ? »
> « Ça dépend du coût de chaque erreur. Pour du dépistage médical ou une alerte alimentaire, un faux négatif est grave : je privilégie le rappel. Pour un filtre anti-spam, bloquer un mail important coûte plus cher que laisser passer un spam : je privilégie la précision.
>
> Le bon réflexe est de chiffrer ces coûts **avec le métier** avant de choisir la métrique. C'est même la première chose que je fais dans un projet. »

### A5. « Pourquoi avez-vous gardé un modèle simple plutôt qu'un modèle complexe ? »
> « Sur mon projet de crédit, la régression logistique a obtenu un ROC-AUC de 0,715, légèrement au-dessus de la forêt aléatoire. Mais au-delà du score, deux raisons ont tranché : elle **explique chaque décision** — indispensable pour un refus de crédit, et exigé par le RGPD — et elle se déploie plus facilement.
>
> Le modèle le plus complexe n'est pas un objectif ; c'est un coût à justifier. »

### A6. « Comment validez-vous une série temporelle ? »
> « Jamais avec un tirage aléatoire : je coupe par date. Sur mon projet, entraînement jusqu'à fin 2023, validation en 2024 pour choisir les rares réglages, et test sur 2025-2026, touché **une seule fois**.
>
> Et je ne touche jamais au test pour comparer des modèles. Si je le faisais, je m'entraînerais dessus sans le dire. »

### A7. « Qu'est-ce qu'un RAG et comment l'évaluez-vous ? »
> « Le RAG, c'est donner au modèle les bons documents au moment de la question, plutôt que de compter sur sa mémoire. Le pipeline : découpage des documents en morceaux, calcul d'embeddings, stockage vectoriel, recherche des extraits pertinents, puis génération avec citations.
>
> L'évaluation se fait en deux temps, et c'est là que beaucoup de candidats se trompent : d'abord la **recherche** — le bon document est-il dans le top-k ? — puis la **génération** — la réponse est-elle fidèle aux extraits et cite-t-elle ses sources ? J'utilise un jeu de 30 questions de référence avec réponses attendues, et je mesure aussi le taux de refus correct, parce qu'un système qui ne dit jamais "je ne trouve pas" est un système qui hallucine. »

### A8. « Comment limitez-vous les hallucinations ? »
> « Par quatre moyens : ancrer la réponse sur des extraits fournis ; donner explicitement le droit de refuser ; exiger des citations vérifiables ; et valider la sortie — si j'attends du JSON, je le valide avec pydantic.
>
> Et une règle de conception : ne jamais confier une décision à un LLM sans validation humaine quand l'action est irréversible ou coûteuse. »

### A9. « Que se passe-t-il si le modèle se dégrade en production ? »
> « Trois causes possibles. La **dérive des données** : les entrées changent — nouveaux marchés, inflation, crise. La **dérive du concept** : la relation entre variables et cible change. La **dérive des prédictions** : la distribution des sorties s'éloigne de la normale.
>
> Le suivi : comparer les distributions d'entrée à celles de l'entraînement, surveiller les sorties, et mesurer la performance réelle dès que les étiquettes arrivent. Les seuils d'alerte doivent être définis **avant** la mise en production, jamais après l'incident.
>
> J'ai une illustration dans mon projet : les prix de 2020-2022 ont créé un régime différent des années précédentes. Un modèle entraîné avant ces crises doit être réentraîné avec une fenêtre glissante — je l'ai écrit dans les limites du projet. »

### A10. « Comment déployez-vous un modèle ? »
> « Pipeline sauvegardé avec joblib, API FastAPI avec validation pydantic des entrées, conteneur Docker, tests automatisés, et CI GitHub Actions qui rejoue l'entraînement et les tests à chaque modification.
>
> Le détail qui compte : j'utilise **exactement la même fonction de construction de variables** entre l'entraînement et l'API. C'est ce qui évite l'écart train/service, plus insidieux que la fuite de données, parce qu'il ne se voit qu'en production. »

### A11. « Pourquoi les modèles d'arbres ne sont-ils pas adaptés à une tendance ? »
> « Parce qu'un arbre ne peut prédire qu'une valeur déjà observée dans son entraînement : il **n'extrapole pas**. Une variable "temps" l'amène à plafonner au prix maximum vu à l'entraînement. C'est pour cela que j'ai retiré la variable de temps dans mon projet et que je travaille sur la **variation** plutôt que sur le niveau — et j'ai laissé la tendance aux modèles de séries temporelles. »

### A12. « Une baseline naïve est meilleure que votre modèle. Pourquoi l'utiliser quand même ? »
> **Question piège : c'est ta crédibilité qui se joue ici.**
> « Les deux. À 1, 3 et 6 mois, je recommande la persistance, parce que c'est elle qui minimise l'erreur sur la période de test : sur des prix alimentaires, la marche aléatoire est très difficile à battre. À 12 mois, mon modèle bat la persistance de 10 %, et le saisonnier de 13 %.
>
> La valeur du travail n'est pas "mon modèle gagne partout", c'est **savoir où il gagne et le dire**. J'ai implémenté ce résultat dans l'API : elle recommande automatiquement la méthode la plus précise selon l'horizon. Un modèle déployé partout malgré des preuves du contraire, c'est du marketing, pas de l'ingénierie. »

### A13. « Quelle est votre plus grosse erreur technique ? »
> « La fuite de données de mon premier jet. Mon MAPE était de 0,2 %, j'étais content pendant dix minutes — puis j'ai trouvé que c'était invraisemblable. J'avais une variable construite avec le prix du mois courant alors que la prévision se fait avant ce mois.
>
> Ce qui compte, c'est ce qu'on fait après : j'ai écrit un test automatisé qui corrompt le présent et vérifie qu'aucune variable ne change. Depuis, la fuite ne peut plus revenir sans casser la CI. »

---

## PARTIE B — Test technique sur table (2 h 30, conditions réelles)

**Énoncé type** (c'est le format le plus courant pour un junior en France/Belgique/Suisse) :

> *Vous disposez d'un fichier `clients.csv` (12 000 lignes) avec des données client et une colonne `resiliation` (1 = le client est parti). Construisez un modèle qui prédit la résiliation, évaluez-le et expliquez vos choix.*

**Ce que le recruteur regarde, par ordre d'importance :**

| Étape | Attendu | Bon réflexe |
|---|---|---|
| 1. Cadrage | comprendre l'objectif métier | demander : « que coûte une résiliation ratée vs une fausse alerte ? » |
| 2. Exploration | 3-4 observations écrites, pas 20 graphiques | regarder le taux de positifs, les valeurs manquantes, les distributions |
| 3. Séparation | **avant toute transformation** | split + stratification |
| 4. Baseline | obligatoire | « toujours non-résilié » puis régression logistique |
| 5. Modélisation | simple d'abord | logistique → forêt / LightGBM |
| 6. Évaluation | la bonne métrique + le seuil | ROC-AUC, PR-AUC, rappel/precision au seuil choisi |
| 7. Interprétation | sens des variables | coefficients ou SHAP, en langage métier |
| 8. Communication | 5 lignes de conclusion | performance, limites, recommandation |

**Grille de notation (100 points) :**
- Cadrage et questions posées : 15
- Absence de fuite (preuve que la séparation précède les transformations) : **20**
- Baseline présente et battue ou expliquée : 15
- Choix de métriques justifié par le coût des erreurs : 15
- Modèle raisonnable et correctement réglé : 15
- Interprétation et honnêteté sur les limites : 20
- **Seuil de réussite : 65/100.** En dessous de 50, retravaille les chapitres 8 et 9 du cours.

**Astuce** : écris tes conclusions **en français**, dans le notebook. Un recruteur privilégie un candidat qui explique à un candidat qui obtient +0,5 % d'AUC.

---

## PARTIE C — Questions RH et questions pièges (7)

### C1. « Pourquoi vous et pas un candidat local ? » *(la plus importante pour toi)*
> « Trois arguments. D'abord la spécialisation : je ne suis pas généraliste, je suis formé et entraîné sur du LLM/RAG et du déploiement, qui est exactement la tension du marché. Ensuite les preuves : API en ligne, tests automatisés, README où je documente même les cas où un modèle naïf me bat — vous pouvez vérifier en dix minutes. Enfin, un profil habitué à travailler avec des ressources contraintes : je code sans GPU toute l'année, je sais prioriser ce qui apporte de la valeur et non ce qui fait joli. Pour une entreprise, ça veut dire quelqu'un qui livre sans avoir besoin d'un environnement idéal. »
>
> ⚠️ **Ne dis jamais** « je suis moins cher » ou « je travaillerai plus ». Ça dévalorise et fait peur.

### C2. « Votre diplôme est une licence ; nous demandons souvent un master. »
> « Je sais, et c'est pourquoi j'ai deux réponses. D'abord la compétence : je peux montrer du code déployé, des tests, des résultats mesurés que vous vérifiez immédiatement. Ensuite la trajectoire : je prépare une candidature en master d'informatique en France pour la rentrée prochaine, avec un dossier que mes projets rendent nettement plus solide. Si vous embauchez aujourd'hui, vous prenez quelqu'un qui apprend vite et qui est déjà opérationnel sur le cœur du travail : les données, les pipelines, l'évaluation. »

### C3. « Avez-vous besoin d'un visa ? Où en êtes-vous ? »
> Réponds **factuellement, sans t'excuser** : « Je réside au Burkina Faso. Pour un poste en France, il existe le passeport talent "salarié qualifié", mais il exige un master, donc mon chemin réaliste est le master d'abord ou le télétravail. Pour un poste en télétravail, aucune démarche n'est nécessaire : je peux être opérationnel immédiatement, avec un décalage horaire d'une heure seulement. »
>
> 💡 Avoir **cette phrase prête** fait la différence : la plupart des candidats se perdent sur ce sujet. Ne mens jamais sur ta situation administrative : ça se vérifie.

### C4. « Vous avez appris en ligne. Comment savez-vous que votre niveau est suffisant ? »
> « Parce que je l'ai confronté à des données réelles que je ne contrôlais pas, et que j'accepte le verdict des faits. Sur 22 656 observations du Programme Alimentaire Mondial, la méthode naïve bat mon modèle à court terme — je l'écris dans mon README. Un cours ne me l'aurait pas appris ; un dataset réel, si.
>
> Le meilleur test reste de faire ce test technique avec vous. »

### C5. « Où vous voyez-vous dans trois ans ? »
> « Dans une équipe où je suis le référent sur une brique précise — probablement l'IA appliquée et le RAG — avec des modèles en production dont je surveille la dérive, et capable de former un junior. Je ne cherche pas à changer de métier tous les ans : je cherche à approfondir un domaine où la demande est structurelle. »

### C6. « Quelle est votre prétention salariale ? »
> « D'après les baromètres 2026, un profil junior en data science se situe autour de 40 à 50 k€ brut annuel en Île-de-France, un peu moins en région, et un AI engineer orienté LLM/RAG plutôt 50-60 k€. Je m'aligne sur cette fourchette, en tenant compte du fait que j'arrive avec un portfolio opérationnel et non à former intégralement. »
>
> ⚠️ **Toujours donner une fourchette documentée**, jamais « je m'adapte à tout ». Citer le marché montre que tu t'es renseigné.

### C7. « Avez-vous des questions pour nous ? »
> Toujours oui. Trois questions qui marquent :
> 1. « Comment mesurez-vous aujourd'hui l'impact des modèles en production ? »
> 2. « Quels modèles tournent déjà en production, et qui s'occupe de la surveillance ? »
> 3. « Sur les six premiers mois, qu'est-ce qui ferait de cette embauche une réussite pour vous ? »

---

## PARTIE D — Les 5 questions qu'on te posera **sur ton projet de prix** (à préparer absolument)

Ton projet est dans ton CV : on va le fouiller. Prépare ces 5 réponses **avec tes propres mots** :

1. **« Résumez-moi ce projet en 60 secondes. »** → besoin métier, données, méthode, résultat chiffré, ce que tu en as appris.
2. **« Pourquoi votre modèle perd-il contre la baseline à 3 mois ? »** → la marche aléatoire des prix à court terme ; la saisonnalité et le retour à la moyenne ne se manifestent qu'à 12 mois (c'est là que le gain de +10 % apparaît).
3. **« Comment avez-vous choisi le seuil de 0,26 de l'alerte ? »** → sur la **validation 2024** uniquement, pour atteindre un rappel cible de 60 % ; le test 2025-2026 n'a servi qu'à constater (60,2 % de rappel obtenu).
4. **« Qu'est-ce que la PR-AUC de 0,266 signifie concrètement ? »** → le taux de base est de 0,114 : le modèle classe environ 2,3 fois mieux que le hasard ; au seuil retenu il détecte 60 % des flambées en signalant 36 % des mois. Utile pour prioriser la surveillance, pas pour décider seul.
5. **« Qu'auriez-vous fait avec plus de temps ? »** → ajouter des variables exogènes (pluviométrie, NDVI, sécurité, carburant) ; produire des intervalles de prédiction (régression quantile) ; mettre en place un suivi de dérive mensuel. *(Ces trois points sont déjà écrits dans les limites du projet — citer son propre README rassure énormément.)*

---

## PARTIE E — Grille d'auto-évaluation

Note-toi honnêtement sur 100, après un entretien blanc :

| Critère | Points | Ma note |
|---|---|---|
| Pitch de 2 minutes fluide et structuré | 10 | |
| J'explique la fuite de données avec **mon** exemple | 12 | |
| Je justifie mes métriques par le coût des erreurs | 12 | |
| Je réponds à « pourquoi un modèle simple ? » sans hésiter | 10 | |
| Je parle de validation temporelle et du jeu de test intact | 12 | |
| J'explique RAG et son évaluation (recherche **et** génération) | 12 | |
| Je parle de dérive et de surveillance sans être vague | 10 | |
| Je réponds au piège « la baseline vous bat » avec assurance | 12 | |
| J'ai 3 questions pertinentes à poser | 5 | |
| Je reste sous 90 secondes par réponse | 5 | |

**Interprétation :**
- **85-100** → tu es prêt. Postule en volume.
- **65-84** → bon niveau, retravaille les critères sous 8 points.
- **50-64** → reprends les chapitres 8, 9 et 22 du cours, refais un entretien blanc.
- **< 50** → normal si tu es au mois 6 du parcours. Continue, reviens dans 2 mois.

---

## PARTIE F — Les 7 erreurs qui font échouer un entretien junior

| Erreur | Conséquence | À faire |
|---|---|---|
| Réciter des définitions de cours | le recruteur décroche | toujours un exemple vécu |
| Annoncer un score sans contexte ni baseline | perte totale de crédibilité | « 0,715 contre 0,524 pour la règle métier » |
| Ne jamais parler des limites | tu parais naïf ou malhonnête | cite spontanément une limite |
| Dire « je ne sais pas » et s'arrêter | occasion manquée | « je ne sais pas encore, voici comment je m'y prendrais » |
| Réponse de 4 minutes | tu perds l'attention | 90 secondes maximum |
| Critiquer son ancien employeur/école | signal d'alerte | reste factuel et tourné vers l'apprentissage |
| Poser zéro question à la fin | manque d'intérêt perçu | 2-3 questions préparées |

---

## 🎯 Ton plan d'entraînement (2 semaines)

| Jour | Action | Durée |
|---|---|---|
| J1 | Mode 1 sur la partie A (questions 1-7), noter ses manques | 1 h |
| J2 | Mode 1 sur la partie A (questions 8-13) | 1 h |
| J3 | Refais ton pitch enregistré, 3 fois, jusqu'à être fluide | 30 min |
| J4 | Test technique chronométré (partie B, conditions réelles) | 2 h 30 |
| J5 | Partie C à voix haute, enregistré | 45 min |
| J6 | Partie D (questions sur ton projet) enregistré | 45 min |
| J7 | Entretien blanc complet avec un partenaire | 1 h |
| J8 | Réécoute tout, remplis la grille de la partie E | 1 h |

> **Le meilleur investissement de ta préparation : enregistre-toi.** On ne corrige bien que ce qu'on a entendu de soi-même.

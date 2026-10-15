# 🎯 Mon projet fil rouge — « AgroDrone Sahel »

**Livrable de la semaine 1** · à copier à la racine de mon dépôt · v1 du 15/10/2026

---

## 1. Le projet en une phrase

> **Analyser automatiquement des images d'un champ (drone ou satellite) pour cartographier
> les zones qui manquent d'eau ou qui sont malades, et dire à l'agriculteur où agir en
> priorité — au lieu de traiter tout le champ à l'aveugle.**

L'idée de départ est **la mienne** : une startup qui survole les champs et analyse chaque
côté du terrain pour détecter la soif et les maladies. Le fil rouge des 52 semaines
consiste à transformer cette idée en **produit réel et démontrable**, en partant de zéro
et sans matériel au départ.

---

## 2. Pourquoi ce projet est le bon choix

| Critère | Mon projet |
|---|---|
| **Utilité réelle** | Au Sahel, l'eau et les intrants coûtent cher : arroser ou traiter uniquement les zones touchées, c'est de l'argent gagné pour l'agriculteur. |
| **Couverture du programme** | Il utilise **tout** : Python, données tabulaires, ML classique, vision par ordinateur, deep learning, géospatial, LLM, déploiement. Aucun chapitre du parcours ne sera « hors sujet ». |
| **Ce que ça dit en entretien** | « J'ai identifié un problème agricole réel, je l'ai modélisé, j'ai entraîné un modèle de segmentation, je l'ai déployé en application, et voici mes résultats honnêtes. » |
| **Différenciation** | La quasi-totalité des datasets publics d'agriculture sont américains ou européens. **Un modèle entraîné sur des cultures sahéliennes (mil, sorgho, niébé, oignon) n'existe presque pas.** C'est mon avantage compétitif — et mon futur argument commercial. |
| **Progression naturelle** | Je peux tout faire **sans drone pendant 6 mois**, puis passer au terrain quand j'ai les compétences et un partenaire. |

---

## 3. ⚠️ La précision technique qui change tout (à comprendre dès maintenant)

Ma phrase de départ mélangeait **deux problèmes différents**. Les séparer, c'est déjà
faire de l'ingénierie :

| Ce que je veux détecter | Comment on le voit | Technologie |
|---|---|---|
| 🌿 **« Il est malade »** | **Visible** : taches, rouille, jaunissement, flétrissement sur les feuilles | **Vision par ordinateur** sur photos normales (RGB) — téléphone, drone ou satellite |
| 💧 **« Il a soif » (stress hydrique)** | ❌ **Invisible à l'œil nu** au début : les feuilles ne jaunissent que 1 à 2 semaines **après** le début du manque d'eau | **Indice spectral NDVI** calculé sur une bande **proche infrarouge (NIR)** — qu'un appareil photo classique ne capture pas |

**Conséquence concrète :** détecter la soif **avant** que ça se voie à l'œil est justement
le cœur de la valeur. On y arrive de deux façons :

1. **Satellite (gratuit, à faire tout de suite)** — Sentinel-2 de l'Agence spatiale
   européenne fournit le proche infrarouge **gratuitement**, tous les 5 jours, à 10 mètres
   de résolution, sur tout le Burkina. On en calcule le **NDVI** (vigueur de la végétation)
   et le **NDWI** (teneur en eau) : c'est ainsi que les entreprises d'agriculture de
   précision détectent le stress hydrique.
2. **Drone (plus tard, avec matériel)** — un drone **RGB classique** (photo normale) ne
   voit **pas** le NIR. Il faut soit un drone multispectral (coûteux), soit se contenter
   du visible : couleur, zones nues, eau stagnante, densité de couverture.

> ✅ **Ma règle de démarrage : les données satellites et satellites/aériennes publiques
> d'abord. Le drone devient la phase de collecte terrain, en trimestre 3-4.**

---

## 4. 🗂️ Les 4 modules (un par trimestre)

### Module 1 — Comprendre et mesurer (semaines 1 à 13 · fondamentaux)
- Python solide, NumPy, pandas, matplotlib, statistiques.
- Télécharger **mes premières images Sentinel-2** au-dessus d'une zone agricole burkinabè
  (par exemple la plaine de Bagré, la zone de Loumbila ou du Sourou).
- **Livrable :** une carte NDVI d'une zone réelle + 3 graphiques + ma première analyse écrite.
  (Oui : dès le trimestre 1, je produis quelque chose d'inédit.)

### Module 2 — Prédire (semaines 14 à 26 · machine learning)
- Régression linéaire → arbres → gradient boosting ; validation honnête, fuite de données.
- Croiser NDVI + météo + sol + calendrier cultural pour **quantifier** le stress hydrique.
- **Livrable :** un modèle qui estime le niveau de stress hydrique d'une parcelle, comparé
  à une baseline simple (et je publie le résultat même si la baseline gagne — c'est ce que
  font les vrais scientifiques).

### Module 3 — Voir (semaines 27 à 39 · deep learning et vision)
- CNN, transfer learning, segmentation d'images (U-Net), augmentation de données.
- Entraîner un modèle de **classification de maladies** (dataset PlantVillage : 54 306 images,
  38 classes) puis le **transférer vers mes propres images** prises au téléphone dans un champ.
- Entraîner un modèle de **segmentation d'anomalies aériennes** (dataset Agriculture-Vision :
  21 061 images de champs vues du ciel, en RGB **et** proche infrarouge, avec des annotations
  d'eau stagnante, de carences et de mauvaises herbes).
- **Livrable :** une image de champ en entrée → une carte colorée des zones à problème en sortie.

### Module 4 — Livrer (semaines 40 à 52 · produit, LLM, MLOps)
- **API** (FastAPI) + **interface web** : je téléverse une image, j'obtiens la carte du champ.
- **Assistant RAG** : « cette zone manque d'eau depuis 8 jours, mil au stade épiaison →
  voici ce qu'il faut faire », avec les fiches techniques locales comme base de connaissances.
- **Déploiement** (Docker, CI/CD), suivi du modèle, coût d'infrastructure.
- **Livrable final :** une démo publique + une page « produit » avec les 3 questions
  business ci-dessous. C'est ma présentation de portfolio ET mon pitch de startup.

---

## 5. 💰 Le plan matériel (honnête, par étapes)

| Étape | Matériel | Coût | Ce que je peux faire |
|---|---|---|---|
| **Maintenant** | Aucun | **0 FCFA** | Satellites gratuits + datasets publics : 100 % du travail technique |
| **Trimestre 3** | Mon smartphone | 0 FCFA | Photos au sol (haut de tige, perche) : jeu de données « maladie » réel |
| **Trimestre 4** | Drone + pilote, ou prêt/partenariat | variable | Collecte aérienne réelle. Une coopérative, une ONG ou une école d'agriculture peut prêter un drone contre un rapport d'analyse |
| **Après le parcours** | Drone multispectral | investissement | Le vrai produit commercial |

**Les 3 questions terrain à poser avant d'investir un franc** (à faire en T2-T3, auprès
d'agriculteurs, coopératives de la région, ONG agricoles, revendeurs d'intrants) :
1. *« Combien vous coûte une année où vous arrosez/traitez tout le champ à l'aveugle ? »*
2. *« Si je vous montrais la carte exacte des zones touchées, vous feriez quoi différemment ? »*
3. *« Qui devrait payer pour ça : l'agriculteur, la coopérative, ou l'acheteur de la récolte ? »*

> Ces trois réponses valent plus que n'importe quel modèle. Un projet qui n'a pas posé
> ces questions est un exercice ; un projet qui les a posées est une **startup**.

---

## 6. 📍 Ma question de départ (une seule phrase)

> **« À partir d'images aériennes ou satellites, peut-on cartographier automatiquement les
> zones d'une parcelle qui sont en stress hydrique ou touchées par une maladie, et le faire
> avec une précision utile à l'agriculteur ? »**

C'est cette phrase que je relis à chaque fin de trimestre pour vérifier que je n'ai pas
dérivé. Elle peut évoluer — mais elle doit rester **précise et répondable**.

---

## 7. ✍️ Ce que je remplis moi-même (maintenant, 10 minutes)

- **Le nom du projet :** AgroDrone Sahel &nbsp;&nbsp; ☐ je le garde &nbsp; ☐ je le change en : ..............................
- **Ma zone d'étude de référence (une région du Burkina) :** ..............................................................
- **La culture que j'étudie en priorité** (mil, sorgho, maïs, niébé, oignon, riz, coton) : ..............................
- **Pourquoi ce sujet me tient à cœur (2 lignes sincères) :**

  > ......................................................................................................................................................
- **Le nom d'**une** personne ou structure que je pourrai questionner (agriculteur, coopérative, ONG, école) :**

  > ......................................................................................................................................................

---

## 8. 🔁 Journal du projet

| Date | Étape franchie | Résultat mesuré |
|---|---|---|
| 15/10/2026 | Idée posée, cadrage écrit, dépôt `ia-parcours` publié | — |
| | | |

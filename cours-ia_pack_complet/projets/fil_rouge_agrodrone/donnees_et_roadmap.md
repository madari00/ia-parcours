# 📡 AgroDrone Sahel — données disponibles et plan des 4 trimestres

> Document de référence. Vérifié le 15/10/2026. Je le relis au début de chaque module.

---

## 1. Les 5 sources de données (toutes gratuites)

| # | Source | Contenu | Taille | Utile pour |
|---|---|---|---|---|
| 1 | **Sentinel-2** (ESA / Copernicus) | Images satellites **multispectrales** (visible + proche infrarouge), **10 m** de résolution, **tous les 5 jours**, couverture mondiale | aucune limite | 🌿 **NDVI** (vigueur) et 💧 **NDWI** (eau) → détecter le **stress hydrique** |
| 2 | **Agriculture-Vision** (CVPR 2020-2025) | **21 061** images aériennes de parcelles (USA, 2019), **4 canaux : RGB + proche infrarouge**, 512×512 px, avec masques annotés par des agronomes : eau stagnante, mauvaises herbes, carences, double semis, ombre de nuage | ~20 Go (extrait plus léger disponible) | 🛰️ apprendre la **segmentation d'anomalies vues du ciel** |
| 3 | **PlantVillage** (Mohanty et al., 2016) | **54 306** photos de feuilles, **38 classes** (saine / maladie), 14 espèces — dont tomate, pomme de terre, raisin, pommier | 658 Mo (IEEE) à 2,2 Go (Hugging Face) | 🍃 apprendre la **classification de maladies** |
| 4 | **NASA POWER** (API) | Météo journalière par coordonnées GPS : **précipitations, température, humidité, rayonnement**, depuis 1981 | API JSON, instantané | 🔗 croiser l'image avec le **contexte climatique** |
| 5 | **WFP / HDX + FAOSTAT + Banque mondiale** | Prix des céréales, rendements, production, données socio-économiques | déjà dans le pack | 📊 la partie **tabulaire** du projet (le « pourquoi ») |

### Comment on y accède concrètement

**1. Sentinel-2 — la plus importante pour commencer**
- Navigateur d'images (aucune installation) : **Copernicus Browser** → `browser.dataspace.copernicus.eu`
- On y dessine la zone du champ, on choisit une date, on télécharge les bandes.
- Pour aller plus loin (des milliers d'images d'un coup) : **Google Earth Engine** (gratuit
  pour la recherche) — c'est le standard utilisé par les pros de la télédétection.

**2. Agriculture-Vision**
- Dépôt officiel : `github.com/SHI-Labs/Agriculture-Vision`
- Téléchargement en ligne de commande (AWS CLI, sans compte) :
  `aws s3 cp s3://intelinair-data-releases/agriculture-vision/cvpr_challenge_2021/supervised supervised --no-sign-request --recursive`
- Extensions et modèles pré-entraînés : `github.com/jingwu6/Extended-Agriculture-Vision-Dataset`
- ⚠️ 20 Go → je commence par un **sous-ensemble** et je travaille sur des tuiles.

**3. PlantVillage** (le plus simple à charger, en trimestre 3)
- Hugging Face : `huggingface.co/datasets/mohanty/PlantVillage` (2,2 Go, CC-BY-SA-3.0)
- ou Kaggle : recherche « PlantVillage » (beaucoup de versions, ~600 Mo)

**4. NASA POWER** — exemple d'appel pour une parcelle près de Ouagadougou :
```
https://power.larc.nasa.gov/api/temporal/daily/point
   ?parameters=PRECTOTCORR,T2M,RH2M&community=AG
   &latitude=12.3714&longitude=-1.5197
   &start=20250101&end=20251231&format=JSON
```
→ renvoie la pluie et la température jour par jour, sans clé d'API.

---

## 2. ⚠️ Les 4 pièges de la télédétection (à connaître **avant** de coder)

| Piège | Ce qui arrive | Le réflexe correct |
|---|---|---|
| **Les nuages** | en saison des pluies, l'image satellite de la date voulue est inutilisable | utiliser des **composites** sur 5-10 jours, ou télécharger un masque de nuages |
| **Le pixel mixte** | un pixel de 10 m contient plusieurs cultures, du sol nu et de l'herbe | travailler par **parcelle**, pas pixel par pixel, et vérifier le terrain |
| **Le décalage temporel** | l'image du 12 mai ne dit rien sur l'état du 12 mai si elle a été prise à 10h30 après une pluie | toujours relier l'image à sa **date + heure** et au calendrier cultural |
| **La fausse corrélation** | « NDVI bas = manque d'eau » — sauf si la cause est une maladie, une carence ou une inondation | mesurer, comparer, et documenter les autres causes possibles |

---

## 3. 🗓️ Le plan des 4 trimestres

### Modules T1 — semaines 1 à 13 : *comprendre et mesurer* (fondamentaux)
| Semaines | Compétence du cours | Application à AgroDrone Sahel |
|---|---|---|
| 1-4 | Python, Git, fichiers | ce cadrage, le dépôt, les premiers scripts |
| 5-8 | NumPy, pandas, graphiques | lire un CSV de prix agricoles, tracer une saisonnalité |
| 9-11 | Statistiques, probabilités | moyenne, variance, corrélation : avant de parler de modèle |
| 12-13 | **Première carte NDVI** | télécharger 2 images Sentinel-2 (saison sèche et saison des pluies), calculer le NDVI, produire une carte |

> 🎯 **Livrable T1 :** une carte NDVI commentée d'**une vraie zone agricole burkinabè**,
> avec 2 dates comparées. Personne dans ma promotion n'aura ça au trimestre 1.

### Modules T2 — semaines 14 à 26 : *prédire* (machine learning)
| Semaines | Compétence | Application |
|---|---|---|
| 14-18 | régression, validation, fuite de données | estimer un indicateur de stress à partir du NDVI, de la pluie et du stade cultural |
| 19-23 | arbres, gradient boosting, SHAP | quelles variables expliquent le plus le stress ? (réponse attendue : la pluie des 15 derniers jours) |
| 24-26 | classification, déséquilibre de classes | alerte binaire : « cette parcelle va passer en stress dans 10 jours » |

> 🎯 **Livrable T2 :** un modèle **+ une baseline honnête**, et un rapport où j'explique
> ce qui marche, ce qui ne marche pas, et pourquoi.

### Modules T3 — semaines 27 à 39 : *voir* (deep learning et vision)
| Semaines | Compétence | Application |
|---|---|---|
| 27-30 | réseau de neurones, PyTorch | premier CNN sur les données tabulaires puis sur images |
| 31-34 | transfer learning (ResNet, EfficientNet) | **classification de maladies** : PlantVillage → puis mes propres photos de terrain |
| 35-39 | segmentation (U-Net), augmentation | **carte des anomalies** sur images aériennes (Agriculture-Vision : RGB + NIR) |

> 🎯 **Livrable T3 :** je donne une image de champ → le modèle renvoie une carte colorée
> des zones à problème, avec un score de confiance.

### Modules T4 — semaines 40 à 52 : *livrer* (produit, LLM, MLOps)
| Semaines | Compétence | Application |
|---|---|---|
| 40-43 | API FastAPI | endpoint : `POST /analyser` (image) → JSON des zones détectées |
| 44-46 | LLM et RAG | assistant : « zone nord : stress hydrique modéré depuis 8 jours, mil en épiaison → conseil » |
| 47-50 | Docker, CI/CD, déploiement | application en ligne, accessible depuis un téléphone |
| 51-52 | portfolio, entretiens | le projet devient ma démonstration principale |

> 🎯 **Livrable final :** une **démo publique** + une page produit avec les 3 questions
> business (dans `cadrage_projet.md`) et les réponses obtenues sur le terrain.

---

## 4. Ce que je fais **cette semaine** (semaine 1)

Rien de technique sur ce projet : je remplis la **section 7** de `cadrage_projet.md`
(nom, zone d'étude, culture, contact terrain). C'est le seul travail demandé — et c'est
le plus important : choisir **une** culture et **une** zone me fera gagner des semaines
plus tard.

**Programme de la semaine 1 :** notebook `01_premiers_pas_python.ipynb` + les 2 exercices
de `semaine_01/`. Le projet fil rouge commence réellement en semaine 5.

---

*Document créé le 15/10/2026 · à relire au début de chaque module.*

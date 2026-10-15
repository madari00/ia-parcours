# 🛰️ AgroDrone Sahel — l'atelier du projet fil rouge

> **Une phrase :** cartographier automatiquement les zones d'une parcelle qui manquent d'eau
> ou qui sont malades, à partir d'images satellites ou de drone.

**Statut :** 🟡 cadrage écrit (semaine 1) · chantier ouvert pour 52 semaines
**Question de départ :** voir `cadrage_projet.md` à la racine du dépôt.

---

## Pourquoi ce dossier existe

Ce dossier grandira **52 semaines**. À chaque nouvelle compétence apprise dans le cours,
je reviens ici et j'ajoute une brique. À la fin, ce dossier contiendra :

```
fil_rouge_agrodrone/
├── README.md                 <- ce fichier (le point d'entrée)
├── donnees_et_roadmap.md     <- sources de données + plan des 4 trimestres
├── donnees/
│   ├── brut/                 <- images satellites / aériennes téléchargées
│   └── prepare/              <- données nettoyées, prêtes pour les modèles
├── notebooks/                <- mes analyses, une par étape
├── src/                      <- le code réutilisable (nettoyage, features, modèles)
├── modeles/                  <- modèles entraînés (exclus de Git, régénérables)
├── app/                      <- API + interface web (trimestre 4)
└── rapports/                 <- cartes, figures, résultats mesurés
```

## Les 5 règles du projet

1. **Une hypothèse avant chaque expérience.** J'écris ce que je pense obtenir *avant* de lancer le code.
2. **Toujours une baseline.** Je compare mon modèle naïf avant tout modèle sophistiqué.
3. **Je publie les échecs.** « La persistance battait mon modèle » est une *découverte*, pas une honte.
4. **Données libres uniquement** (ou collectées avec accord écrit du propriétaire du champ).
5. **Un résultat mesuré** (chiffre + intervalle) vaut mieux que dix affirmations.

## Données et éthique

Aucune image aérienne du Burkina Faso n'est publiée sans l'accord des propriétaires des
parcelles. Les images de drone sont conservées localement, jamais publiées avec des
coordonnées GPS précises de parcelles privées.

## Licences à respecter

| Source | Licence | Obligation |
|---|---|---|
| Sentinel-2 (ESA) | Copernicus, libre | citer « ESA / Copernicus » |
| Agriculture-Vision | usage recherche | citer Wu et al. (2023) |
| PlantVillage | CC-BY-SA-3.0 | citer Mohanty et al. (2016) |

---

*Dernière mise à jour : 15/10/2026 (semaine 1).*

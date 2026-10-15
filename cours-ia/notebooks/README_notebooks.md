# 📓 Notebooks d'exercices

Ces notebooks sont **volontairement partiels** : ils contiennent le squelette et les consignes, mais **c'est à toi d'écrire le code manquant**. C'est ainsi qu'on apprend (règle 30/70).

## Comment les utiliser

1. **Option A (recommandée) — Google Colab :** ouvre [colab.research.google.com](https://colab.research.google.com) → *Importer un notebook* → dépose le fichier `.ipynb`. Tu n'as rien à installer.
2. **Option B — en local :**
   ```bash
   pip install jupyter numpy pandas scikit-learn matplotlib
   jupyter notebook
   ```
   Puis ouvre le fichier `.ipynb`.

## Ordre de travail

| Notebook | À faire après | Contenu |
|---|---|---|
| `01_premiers_pas_python.ipynb` | Chapitre 0-1 | Python, fonctions, structures, fichiers |
| `02_numpy.ipynb` | Chapitre 2 | Tableaux, vectorisation, normalisation |
| `03_gradient.ipynb` | Chapitre 5 | Écrire la descente de gradient de A à Z |
| `04_machine_learning.ipynb` | Chapitres 8-11 | Workflow ML complet + comparaison de modèles |
| `05_llm_rag.ipynb` | Chapitre 21-22 | Prompt engineering et recherche sémantique (sans clé API) |
| `06_deploiement.ipynb` | Chapitre 25 | Préparer un modèle pour une API |

## Règles de travail

- **Retaper** le code, ne pas copier-coller les solutions trouvées en ligne.
- Écrire dans le notebook, en **français**, ce que tu observes après chaque résultat. Un notebook de portfolio contient toujours des commentaires d'analyse.
- **Sauvegarder** chaque notebook terminé dans ton dépôt GitHub (`git add` / `git commit` / `git push`).
- Si un notebook plante : lis le message d'erreur **en entier** (la dernière ligne dit quoi, la première dit où).

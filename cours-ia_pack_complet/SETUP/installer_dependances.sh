#!/usr/bin/env bash
# Installation des dépendances par phase — macOS / Linux
# Usage : bash installer_dependances.sh [fondations|ml|dl|llm|tout]
set -e
PHASE="${1:-fondations}"
jouer() { echo ""; echo "▶ $1"; eval "$2"; }

case "$PHASE" in
  fondations) jouer "Phase 1 — Fondations" "pip install -r requirements_fondations.txt" ;;
  ml)         jouer "Phase 2 — Machine Learning" "pip install -r requirements_ml.txt" ;;
  dl)         jouer "Phase 3 — Deep Learning (CPU)" \
                   "pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu && pip install -r requirements_deep_learning.txt" ;;
  llm)        jouer "Phase 4 — LLM, RAG, MLOps, déploiement" "pip install -r requirements_llm_deploiement.txt" ;;
  tout)       "$0" fondations; "$0" ml; "$0" dl; "$0" llm ;;
  *) echo "Usage : bash installer_dependances.sh [fondations|ml|dl|llm|tout]"; exit 1 ;;
esac

echo ""
echo "✅ Terminé. Vérifie avec : python verifier_environnement.py"

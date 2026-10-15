# Installation des dépendances par phase — Windows (PowerShell)
# Usage : .\installer_dependances.ps1 fondations
param([ValidateSet("fondations","ml","dl","llm","tout")][string]$Phase = "fondations")

function Invoke-Etape($titre, $commande) {
    Write-Host "`n> $titre" -ForegroundColor Cyan
    Invoke-Expression $commande
}

switch ($Phase) {
    "fondations" { Invoke-Etape "Phase 1 - Fondations" "pip install -r requirements_fondations.txt" }
    "ml"         { Invoke-Etape "Phase 2 - Machine Learning" "pip install -r requirements_ml.txt" }
    "dl"         {
        Invoke-Etape "Phase 3 - Deep Learning (CPU)" "pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu"
        Invoke-Etape "Phase 3 - Bibliothèques NLP" "pip install -r requirements_deep_learning.txt"
    }
    "llm"        { Invoke-Etape "Phase 4 - LLM, RAG, MLOps" "pip install -r requirements_llm_deploiement.txt" }
    "tout" {
        & $PSCommandPath fondations
        & $PSCommandPath ml
        & $PSCommandPath dl
        & $PSCommandPath llm
    }
}

Write-Host "`nTermine. Verifie avec : python verifier_environnement.py" -ForegroundColor Green

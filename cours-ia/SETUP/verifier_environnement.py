#!/usr/bin/env python3
"""Diagnostic de ton environnement de travail.

Usage :
    python verifier_environnement.py

Le script vérifie Python, pip, Git, les bibliothèques par étape, et t'indique
exactement quoi installer. Aucune connexion internet n'est nécessaire.
"""
from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path

# --------------------------------------------------------------------------- #
# Configuration : ce que chaque étape du parcours exige
# --------------------------------------------------------------------------- #
ETAPES = [
    ("T1 · Fondations (semaines 1-13)", "requis",
     ["numpy", "pandas", "matplotlib"]),
    ("T1 · Optionnel (notebooks, exploration)", "confort",
     ["jupyter", "seaborn", "openpyxl"]),
    ("T2 · Machine Learning (semaines 14-26)", "requis",
     ["sklearn", "joblib"]),
    ("T2 · Modèles d'ensemble (semaines 20-26)", "requis",
     ["lightgbm", "xgboost"]),
    ("T2 · Interprétabilité (semaines 24-26)", "confort",
     ["shap"]),
    ("T3 · Deep Learning (semaines 27-39)", "requis",
     ["torch"]),
    ("T3 · Vision (semaines 32-34)", "requis",
     ["torchvision"]),
    ("T3 · Modèles pré-entraînés (semaines 38-39)", "requis",
     ["transformers", "datasets"]),
    ("T4 · RAG (semaines 42-44)", "requis",
     ["sentence_transformers", "faiss"]),
    ("T4 · Interfaces et déploiement (semaines 44-50)", "requis",
     ["streamlit", "fastapi", "uvicorn", "pydantic"]),
    ("T4 · MLOps (semaines 47-48)", "confort",
     ["mlflow", "pytest", "evidently"]),
]

# nom du paquet pip pour un module dont le nom diffère
PAQUET_PIP = {
    "sklearn": "scikit-learn",
    "sentence_transformers": "sentence-transformers",
    "faiss": "faiss-cpu",
    "torch": "torch (version CPU suffit pour apprendre)",
    "torchvision": "torchvision",
    "jupyter": "jupyterlab",
    "uvicorn": "uvicorn[standard]",
}

VERT, ROUGE, JAUNE, GRIS, GRAS, RAZ = (
    "\033[92m", "\033[91m", "\033[93m", "\033[90m", "\033[1m", "\033[0m"
)


def titre(texte: str) -> None:
    print(f"\n{GRAS}{texte}{RAZ}")
    print("─" * max(len(texte), 52))


def version_module(nom: str) -> str | None:
    """Renvoie la version du module, ou None s'il est absent."""
    if importlib.util.find_spec(nom) is None:
        return None
    try:
        paquet = __import__(nom)
        return getattr(paquet, "__version__", "installé")
    except Exception:  # noqa: BLE001  (un module présent mais cassé compte comme absent)
        return None


def commande(args: list[str], cwd: Path | None = None) -> tuple[int, str]:
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=12, cwd=cwd)
        return r.returncode, (r.stdout or r.stderr).strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return 1, ""


def main() -> int:
    print(f"{GRAS}Diagnostic de l'environnement — parcours IA{RAZ}")
    print(f"{GRIS}Date : {__import__('datetime').date.today():%d/%m/%Y}{RAZ}")
    problemes: list[str] = []

    # ------------------------------------------------------------------ #
    # 1. Python
    # ------------------------------------------------------------------ #
    titre("1. Python")
    majeur, mineur = sys.version_info[:2]
    print(f"  version : {sys.version.split()[0]}  ({sys.executable})")
    if (majeur, mineur) >= (3, 10):
        print(f"  {VERT}✓ version suffisante{RAZ}")
    else:
        print(f"  {ROUGE}✗ Python 3.10 minimum requis{RAZ} → installe https://www.python.org/downloads/")
        problemes.append("Python trop ancien")

    pip_dispo = importlib.util.find_spec("pip") is not None or shutil.which("pip") is not None
    print(f"  pip    : {'✓ disponible' if pip_dispo else '✗ absent'}")

    # ------------------------------------------------------------------ #
    # 2. Git et GitHub
    # ------------------------------------------------------------------ #
    titre("2. Git")
    git = shutil.which("git")
    if git:
        code_ver, sortie = commande(["git", "--version"])
        print(f"  {VERT}✓{RAZ} {sortie}")

        # identité configurée ?
        _, nom = commande(["git", "config", "--global", "user.name"])
        _, mail = commande(["git", "config", "--global", "user.email"])
        if nom and mail:
            print(f"  {VERT}✓{RAZ} identité : {nom} <{mail}>")
        else:
            print(f"  {ROUGE}✗ identité Git non configurée{RAZ} — tes commits seraient anonymes.")
            print(f"    {GRIS}git config --global user.name \"Prenom Nom\"{RAZ}")
            print(f"    {GRIS}git config --global user.email \"ton.email@exemple.com\"{RAZ}")
            problemes.append("identité Git à configurer")
    else:
        print(f"  {ROUGE}✗ Git absent{RAZ} → https://git-scm.com/downloads")
        problemes.append("Git à installer")

    # ------------------------------------------------------------------ #
    # 3. Éditeur (VS Code)
    # ------------------------------------------------------------------ #
    titre("3. Éditeur")
    code = shutil.which("code") or shutil.which("code.cmd")
    if code:
        print(f"  {VERT}✓{RAZ} VS Code détecté (commande « code » disponible)")
        _, extensions = commande([code, "--list-extensions"])
        attendues = {
            "ms-python.python": "Python",
            "ms-python.vscode-pylance": "Pylance (autocomplétion)",
            "ms-toolsai.jupyter": "Jupyter (notebooks dans VS Code)",
            "charliermarsh.ruff": "Ruff (qualité de code)",
            "eamodio.gitlens": "GitLens (historique Git)",
        }
        installees = set(extensions.split()) if extensions else set()
        for identifiant, nom in attendues.items():
            if identifiant in installees:
                print(f"    {VERT}✓{RAZ} {nom}")
            else:
                print(f"    {JAUNE}·{RAZ} {nom} manquante → code --install-extension {identifiant}")
    else:
        print(f"  {JAUNE}·{RAZ} VS Code détecté par l'interface graphique mais pas par la ligne de commande.")
        print(f"    {GRIS}Dans VS Code : Ctrl+Shift+P → « Shell Command: Install 'code' command in PATH »{RAZ}")
        print(f"    {GRIS}(tu as déjà VS Code : passe simplement à la section 4){RAZ}")

    # ------------------------------------------------------------------ #
    # 4. Bibliothèques, étape par étape
    # ------------------------------------------------------------------ #
    total_ok = total_req = 0
    for etape, niveau, modules in ETAPES:
        titre(f"4. {etape}")
        manquants = []
        for mod in modules:
            v = version_module(mod)
            etiquette = "requis" if niveau == "requis" else "confort"
            if v:
                print(f"  {VERT}✓{RAZ} {mod:<22s} {v}{GRIS}  [{etiquette}]{RAZ}")
            else:
                print(f"  {ROUGE}✗{RAZ} {mod:<22s} absent{GRIS}  [{etiquette}]{RAZ}")
                manquants.append(PAQUET_PIP.get(mod, mod))
        if manquants:
            commande_pip = "pip install " + " ".join(manquants)
            print(f"  → {GRAS}{commande_pip}{RAZ}")
            if niveau == "requis":
                problemes.append(f"{etape} : {', '.join(manquants)}")
        if niveau == "requis":
            total_req += len(modules)
            total_ok += len(modules) - len(manquants)

    # ------------------------------------------------------------------ #
    # 5. Environnement virtuel actif ?
    # ------------------------------------------------------------------ #
    titre("5. Environnement virtuel")
    dans_venv = sys.prefix != sys.base_prefix
    if dans_venv:
        print(f"  {VERT}✓{RAZ} environnement virtuel actif : {sys.prefix}")
    else:
        print(f"  {JAUNE}·{RAZ} tu utilises le Python global (pas de venv).")
        print(f"    Ce n'est pas bloquant pour apprendre, mais prends l'habitude :")
        print(f"    {GRIS}python -m venv .venv{RAZ}")
        print(f"    {GRIS}# Windows : .venv\\Scripts\\activate   |   macOS/Linux : source .venv/bin/activate{RAZ}")

    # ------------------------------------------------------------------ #
    # 6. Dossiers du parcours
    # ------------------------------------------------------------------ #
    titre("6. Dépôt du parcours")
    ici = Path.cwd()
    if (ici / ".git").exists():
        print(f"  {VERT}✓{RAZ} dépôt Git détecté dans {ici.name}")
        _, branche = commande(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=ici)
        _, commits = commande(["git", "rev-list", "--count", "HEAD"], cwd=ici)
        if commits and commits.isdigit():
            print(f"    branche « {branche} » · {commits} commit(s)")
        _, distant = commande(["git", "remote", "-v"], cwd=ici)
        print(f"    dépôt distant : {'✓ configuré' if distant else '✗ aucun (git remote add origin ...)'}")
    else:
        print(f"  {JAUNE}·{RAZ} pas de dépôt Git ici ({ici}).")
        print(f"    {GRIS}git init && git branch -M main{RAZ}")

    # ------------------------------------------------------------------ #
    # Synthèse
    # ------------------------------------------------------------------ #
    titre("Synthèse")
    if problemes:
        print(f"  {ROUGE}{len(problemes)} point(s) à corriger avant de continuer :{RAZ}")
        for p in problemes:
            print(f"    • {p}")
        print(f"\n  {GRIS}Astuce : copie-colle simplement les lignes « pip install … » ci-dessus.{RAZ}")
    else:
        print(f"  {VERT}✓ tout est prêt : {total_ok}/{total_req} bibliothèques requises installées.{RAZ}")
        print(f"  {GRIS}Tu peux attaquer la semaine 1 du plan.{RAZ}")

    print(f"\n{GRIS}Note : les bibliothèques des phases suivantes ne sont pas nécessaires tout de suite.")
    print(f"Installe-les la semaine où tu en as besoin — sauf si ta connexion est irrégulière,{RAZ}")
    print(f"{GRIS}auquel cas télécharge-les à l'avance (voir 00_Prerequis_et_environnement.md, section 5).{RAZ}\n")
    return 1 if problemes else 0


if __name__ == "__main__":
    sys.exit(main())

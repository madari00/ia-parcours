#!/usr/bin/env python3
"""Diagnostic de ton environnement de travail.

Usage (Windows PowerShell) :
    python verifier_environnement.py
    python SETUP\\verifier_environnement.py     # si tu es à la racine du parcours

Le script vérifie Python, Git, les extensions VS Code, puis chaque phase
bibliothèque par bibliothèque, et te donne les commandes exactes à copier.
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
    ("T1 · Fondations (semaines 1-13)", "requis", ["numpy", "pandas", "matplotlib"]),
    ("T1 · Confort (notebooks, exploration)", "confort", ["jupyter", "seaborn", "openpyxl"]),
    ("T2 · Machine Learning (semaines 14-26)", "requis", ["sklearn", "joblib"]),
    ("T2 · Modèles d'ensemble (semaines 20-26)", "requis", ["lightgbm", "xgboost"]),
    ("T2 · Interprétabilité (semaines 24-26)", "confort", ["shap"]),
    ("T3 · Deep Learning (semaines 27-39)", "requis", ["torch"]),
    ("T3 · Vision (semaines 32-34)", "requis", ["torchvision"]),
    ("T3 · Modèles pré-entraînés (semaines 38-39)", "requis", ["transformers", "datasets"]),
    ("T4 · RAG (semaines 42-44)", "requis", ["sentence_transformers", "faiss"]),
    ("T4 · Interfaces et déploiement (semaines 44-50)", "requis",
     ["streamlit", "fastapi", "uvicorn", "pydantic"]),
    ("T4 · MLOps (semaines 47-48)", "confort", ["mlflow", "pytest", "evidently"]),
]

# Nom du paquet pip quand il diffère du nom du module
PAQUET_PIP = {
    "sklearn": "scikit-learn",
    "sentence_transformers": "sentence-transformers",
    "faiss": "faiss-cpu",
    "torch": "torch",
    "torchvision": "torchvision",
    "jupyter": "jupyterlab",
    "uvicorn": "uvicorn[standard]",
}

# Bibliothèques sensibles aux versions récentes de Python
SENSIBLES_3_14 = ["lightgbm", "xgboost", "shap", "torch", "torchvision",
                  "transformers", "datasets", "faiss", "sentence_transformers"]

VERT, ROUGE, JAUNE, CYAN, GRIS, GRAS, RAZ = (
    "\033[92m", "\033[91m", "\033[93m", "\033[96m", "\033[90m", "\033[1m", "\033[0m"
)

# Pas de couleurs si la sortie est redirigée ou si le terminal ne les gère pas
if not sys.stdout.isatty():
    VERT = ROUGE = JAUNE = CYAN = GRIS = GRAS = RAZ = ""


def titre(texte: str) -> None:
    print(f"\n{GRAS}{texte}{RAZ}")
    print("─" * max(len(texte), 52))


def version_module(nom: str) -> str | None:
    """Renvoie la version du module, ou None s'il est absent/cassé."""
    if importlib.util.find_spec(nom) is None:
        return None
    try:
        return getattr(__import__(nom), "__version__", "installé")
    except Exception:  # noqa: BLE001
        return None


def lire_pyvenv_cfg(prefix: str) -> dict[str, str]:
    """Lit le fichier pyvenv.cfg d'un environnement virtuel.

    Il contient notamment la version de Python utilisée à la création (clé
    « version ») et la commande d'origine (clé « command »), ce qui permet de
    détecter un venv créé avec une version inadaptée ou déplacé depuis.
    """
    cfg = Path(prefix) / "pyvenv.cfg"
    if not cfg.exists():
        return {}
    contenu: dict[str, str] = {}
    for ligne in cfg.read_text(errors="ignore").splitlines():
        if "=" in ligne:
            cle, valeur = ligne.split("=", 1)
            contenu[cle.strip().lower()] = valeur.strip()
    return contenu


def commande(args: list[str], cwd: Path | None = None) -> tuple[int, str]:
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=15, cwd=cwd,
                           shell=False)
        return r.returncode, (r.stdout or r.stderr).strip()
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return 1, ""


def main() -> int:
    print(f"{GRAS}Diagnostic de l'environnement — parcours IA{RAZ}")
    print(f"{GRIS}Système : {sys.platform} · Date : {__import__('datetime').date.today():%d/%m/%Y}{RAZ}")

    problemes: list[str] = []        # bloquant
    avertissements: list[str] = []   # non bloquant, mais à traiter

    # ================================================================== #
    # 1. Python
    # ================================================================== #
    titre("1. Python")
    majeur, mineur = sys.version_info[:2]
    version = f"{majeur}.{mineur}.{sys.version_info[2]}"
    print(f"  version  : {version}")
    print(f"  exécutable : {sys.executable}")

    if (majeur, mineur) < (3, 10):
        print(f"  {ROUGE}✗ Python 3.10 minimum requis{RAZ} → https://www.python.org/downloads/")
        problemes.append("Python trop ancien (3.10 minimum)")
    elif (majeur, mineur) >= (3, 14):
        print(f"  {VERT}✓{RAZ} suffisant pour la Partie 1 (semaines 1-13)")
        print(f"  {JAUNE}⚠ MAIS Python {majeur}.{mineur} est très récent : plusieurs bibliothèques")
        print(f"    des phases 2 à 4 n'ont pas encore de version compatible :")
        print(f"    {', '.join(SENSIBLES_3_14[:5])}…{RAZ}")
        print(f"  {CYAN}→ Recommandation : installer Python 3.12 À CÔTÉ, sans toucher à {majeur}.{mineur}{RAZ}")
        print(f"    {GRIS}winget install --id Python.Python.3.12 -e{RAZ}")
        print(f"    {GRIS}Puis : py -3.12 -m venv .venv{RAZ}")
        print(f"    {GRIS}Détails : SETUP/DEPANNAGE_WINDOWS.md, section 2{RAZ}")
        avertissements.append(f"Python {majeur}.{mineur} : installer 3.12 pour les phases 2 à 4")
    elif (majeur, mineur) >= (3, 13):
        print(f"  {VERT}✓{RAZ} version correcte (3.13 fonctionne pour tout le parcours)")
        print(f"    {GRIS}Si une bibliothèque refuse de s'installer, 3.12 est la valeur la plus sûre.{RAZ}")
    else:
        print(f"  {VERT}✓{RAZ} version idéale pour ce parcours")

    # Liste des Python installés (Windows uniquement)
    if sys.platform.startswith("win"):
        code, sortie = commande(["py", "-0"])
        if code == 0 and sortie:
            print(f"  {GRIS}versions installées (lanceur py) :{RAZ}")
            for ligne in sortie.splitlines():
                print(f"    {ligne}")

    pip_ok = importlib.util.find_spec("pip") is not None or shutil.which("pip")
    print(f"  pip      : {'✓ disponible' if pip_ok else '✗ absent → python -m ensurepip --upgrade'}")

    # Indique si on est dans un environnement virtuel
    dans_venv = sys.prefix != sys.base_prefix
    print(f"  venv     : {'✓ actif (' + Path(sys.prefix).name + ')' if dans_venv else '· non actif'}")

    if dans_venv:
        cfg = lire_pyvenv_cfg(sys.prefix)
        version_base = cfg.get("version", "")
        print(f"  venv base : Python {version_base or '?'}  ({cfg.get('home', 'chemin inconnu')})")

        # a) version de base trop récente ?
        if version_base:
            try:
                mm = tuple(int(x) for x in version_base.split(".")[:2])
                if mm >= (3, 13):
                    print(f"  {JAUNE}⚠ cet environnement a été créé avec Python {version_base}.{RAZ}")
                    print(f"    Les bibliothèques des semaines 20 à 42 risquent de refuser de s'installer.")
                    print(f"  {CYAN}→ Recrée-le avec Python 3.12 :{RAZ}")
                    print(f"    {GRIS}deactivate ; Remove-Item -Recurse -Force .venv{RAZ}")
                    print(rf"    {GRIS}py -3.12 -m venv .venv ; .\.venv\Scripts\Activate.ps1{RAZ}")
                    avertissements.append(f"venv créé avec Python {version_base} → à recréer en 3.12")
            except ValueError:
                pass

        # b) venv déplacé depuis sa création ?
        commande_creation = cfg.get("command", "")
        if commande_creation and sys.prefix not in commande_creation:
            print(f"  {JAUNE}⚠ ce venv a été DÉPLACÉ depuis sa création.{RAZ}")
            print(f"    Créé à l'emplacement indiqué dans : {commande_creation}")
            print(f"    Emplacement actuel : {sys.prefix}")
            print(f"  {CYAN}→ Les venvs ne se déplacent pas proprement : recrée-le sur place.{RAZ}")
            avertissements.append("venv déplacé → à recréer dans son dossier définitif")

    # ================================================================== #
    # 2. Git
    # ================================================================== #
    titre("2. Git (le logiciel, différent du site GitHub)")
    git = shutil.which("git")
    if git:
        _, sortie = commande(["git", "--version"])
        print(f"  {VERT}✓{RAZ} {sortie}")

        _, nom = commande(["git", "config", "--global", "user.name"])
        _, mail = commande(["git", "config", "--global", "user.email"])
        if nom and mail:
            print(f"  {VERT}✓{RAZ} identité : {nom} <{mail}>")
            if "@users.noreply.github.com" not in mail and "gmail" in mail.lower():
                print(f"    {GRIS}Rappel : cet email doit être vérifié sur ton compte GitHub pour que "
                      f"tes commits y apparaissent.{RAZ}")
        else:
            print(f"  {ROUGE}✗ identité Git non configurée{RAZ} → tes commits seraient anonymes.")
            print(f'    {GRIS}git config --global user.name "Prenom Nom"{RAZ}')
            print(f'    {GRIS}git config --global user.email "email de ton compte GitHub"{RAZ}')
            problemes.append("identité Git à configurer")
    else:
        print(f"  {ROUGE}✗ Git n'est pas installé{RAZ} — un compte GitHub ne suffit pas,")
        print(f"    il faut le logiciel Git sur ta machine.")
        print(f"  {CYAN}→ Solution (5 min) :{RAZ}")
        print(f"    {GRAS}winget install --id Git.Git -e --source winget{RAZ}")
        print(f"    {GRIS}ou https://git-scm.com/download/win{RAZ}")
        print(f"    {JAUNE}Puis FERME et ROUVRE PowerShell avant de retester.{RAZ}")
        print(f"    {GRIS}Détails : SETUP/DEPANNAGE_WINDOWS.md, section 1{RAZ}")
        problemes.append("Git à installer")

    # ================================================================== #
    # 3. VS Code et extensions
    # ================================================================== #
    titre("3. VS Code")
    code = shutil.which("code") or shutil.which("code.cmd")
    if code:
        print(f"  {VERT}✓{RAZ} VS Code accessible en ligne de commande")
        _, extensions = commande([code, "--list-extensions"])
        attendues = {
            "ms-python.python": "Python",
            "ms-python.vscode-pylance": "Pylance (autocomplétion, détection d'erreurs)",
            "ms-toolsai.jupyter": "Jupyter (notebooks .ipynb)",
            "charliermarsh.ruff": "Ruff (qualité de code)",
            "eamodio.gitlens": "GitLens (historique Git)",
        }
        installees = set(extensions.split()) if extensions else set()
        manquantes = []
        for identifiant, nom in attendues.items():
            if identifiant in installees:
                print(f"    {VERT}✓{RAZ} {nom}")
            else:
                print(f"    {JAUNE}·{RAZ} {nom} → code --install-extension {identifiant}")
                manquantes.append(nom)
        if manquantes:
            avertissements.append(f"{len(manquantes)} extension(s) VS Code à installer")
    else:
        print(f"  {JAUNE}·{RAZ} VS Code présent (interface) mais commande « code » absente du PATH.")
        print(f"    {GRIS}Dans VS Code : Ctrl+Shift+P → « Shell Command: Install 'code' command in PATH »{RAZ}")
        avertissements.append("commande « code » non disponible dans le terminal")

    # ================================================================== #
    # 4. Bibliothèques, phase par phase
    # ================================================================== #
    total_ok = total_req = 0
    phase1_ok = True
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
            print(f"  → {GRAS}pip install {' '.join(manquants)}{RAZ}")
            if niveau == "requis":
                if etape.startswith("T1"):
                    phase1_ok = False
                else:
                    problemes.append(f"{etape.split('(')[0].strip()} : {', '.join(manquants)}")
            # les bibliothèques des phases suivantes ne sont pas des « problèmes »
        if niveau == "requis":
            total_req += len(modules)
            total_ok += len(modules) - len(manquants)

    # ================================================================== #
    # 5. Dépôt du parcours
    # ================================================================== #
    titre("5. Dossier de travail")
    ici = Path.cwd()
    if (ici / ".git").exists() and git:
        print(f"  {VERT}✓{RAZ} dépôt Git dans « {ici.name} »")
        _, branche = commande(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=ici)
        _, commits = commande(["git", "rev-list", "--count", "HEAD"], cwd=ici)
        if commits and commits.isdigit():
            print(f"    branche « {branche} » · {commits} commit(s)")
        _, distant = commande(["git", "remote", "-v"], cwd=ici)
        print(f"    dépôt distant : {'✓ configuré' if distant else '· aucun (git remote add origin ...)'}")
    else:
        print(f"  {JAUNE}·{RAZ} pas encore de dépôt Git dans {ici}")
        print(f"    {GRIS}Normal si tu débutes : git init → git add . → git commit -m \"feat: ...\"{RAZ}")
    if "download" in str(ici).lower() or "téléchargement" in str(ici).lower():
        print(f"  {JAUNE}⚠{RAZ} ton dossier est dans « Téléchargements », qui peut être nettoyé par Windows.")
        print(f"    {CYAN}→ Déplace-le vers Documents (voir DEPANNAGE_WINDOWS.md, section 5){RAZ}")
        avertissements.append("dossier de travail à déplacer hors de Téléchargements")

    # ================================================================== #
    # Synthèse
    # ================================================================== #
    titre("Synthèse")
    if not phase1_ok:
        print(f"  {ROUGE}⛔ Il manque des bibliothèques essentielles à la Partie 1.{RAZ}")
    if problemes:
        print(f"  {ROUGE}{len(problemes)} point(s) à corriger :{RAZ}")
        for p in problemes:
            print(f"    • {p}")
    if avertissements:
        print(f"  {JAUNE}{len(avertissements)} avertissement(s) — non bloquant :{RAZ}")
        for a in avertissements:
            print(f"    • {a}")
    if not problemes and not avertissements:
        print(f"  {VERT}✓ tout est prêt ({total_ok}/{total_req} bibliothèques requises installées).{RAZ}")
        print(f"  {GRIS}Tu peux attaquer la semaine 1 du plan.{RAZ}")

    if not problemes and not total_ok:
        pass
    elif not problemes:
        print(f"\n  {VERT}✓ Bibliothèques requises installées : {total_ok}/{total_req}.{RAZ}")

    print(f"\n{GRIS}Rappels utiles :{RAZ}")
    print(f"{GRIS}  • n'installe que les bibliothèques de la phase en cours ;{RAZ}")
    print(f"{GRIS}  • après toute installation d'un logiciel, FERME et ROUVRE le terminal ;{RAZ}")
    print(f"{GRIS}  • en cas de doute : SETUP/DEPANNAGE_WINDOWS.md{RAZ}\n")

    return 1 if (problemes or not phase1_ok) else 0


if __name__ == "__main__":
    sys.exit(main())

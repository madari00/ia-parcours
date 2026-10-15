"""Démonstration : comment lire un fichier .env en Python, proprement.

⚠️ CE SCRIPT N'EST PAS NÉCESSAIRE AVANT LA SEMAINE 42.
   Il est là pour que tu voies la bonne pratique quand ce moment arrivera.

Préparation (semaine 42) :
    pip install python-dotenv
    copy .env.example .env      # Windows  (puis colle ta vraie clé dans .env)
"""
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
    note = "fichier .env chargé"
except ImportError:
    note = "python-dotenv absent (pip install python-dotenv) — on lit les variables système"

# On essaie plusieurs fournisseurs, dans l'ordre
CANDIDATS = ["MISTRAL_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_API_KEY", "OLLAMA_BASE_URL"]

trouve = None
for nom in CANDIDATS:
    valeur = os.getenv(nom)
    if valeur:
        # On n'affiche JAMAIS la clé en entier, même dans un terminal
        apercu = valeur[:4] + "…" + valeur[-4:] if len(valeur) > 12 else "***"
        print(f"  ✓ {nom:20s} = {apercu}  (longueur {len(valeur)})")
        trouve = nom
    else:
        print(f"  · {nom:20s} non défini")

print(f"\nÉtat : {note}")
if trouve:
    print(f"✅ Configuration prête : le code peut utiliser {trouve}.")
else:
    print("ℹ️  Aucune clé définie — normal avant la semaine 42.")
    print("   Alternative gratuite et locale : installe Ollama (https://ollama.com),")
    print("   puis `ollama pull mistral`, sans aucune clé d'API.")

# 🛠️ Règles à ne jamais oublier :
#  1. La clé ne s'écrit JAMAIS dans un fichier .py ni dans un notebook.
#  2. Le fichier .env est TOUJOURS dans .gitignore (déjà fait ici).
#  3. Un .env.example avec de fausses valeurs, lui, se partage : il documente
#     les variables attendues sans révéler aucun secret.
#  4. Si une clé fuite sur GitHub : révoque-la immédiatement chez le fournisseur.
#     Supprimer le fichier ne suffit pas, elle reste dans l'historique Git.

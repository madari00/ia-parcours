"""Semaine 1 — Exercice 1 : convertisseur FCFA / euro.

Objectif : premier script versionné avec Git. Lance-le avec :
    python semaine_01/exercice_convertisseur.py
"""

TAUX = 655.957  # 1 euro = 655,957 FCFA (parité fixe de l'UEMOA)


def fcfa_vers_euro(montant_fcfa: float) -> float:
    """Convertit un montant en FCFA vers l'euro, arrondi au centime."""
    return round(montant_fcfa / TAUX, 2)


def euro_vers_fcfa(montant_euro: float) -> float:
    """Convertit un montant en euro vers le FCFA."""
    return round(montant_euro * TAUX, 2)


def afficher(montant_fcfa: float) -> str:
    """Renvoie une phrase lisible pour un montant en FCFA."""
    return f"{montant_fcfa:,.0f} FCFA = {fcfa_vers_euro(montant_fcfa):,.2f} EUR".replace(",", " ")


if __name__ == "__main__":
    # Tests rapides : si une assertion échoue, le script s'arrête et te dit pourquoi.
    assert fcfa_vers_euro(655.957) == 1.0, "1 euro doit valoir 655,957 FCFA"
    assert fcfa_vers_euro(0) == 0.0, "0 FCFA doit valoir 0 euro"
    assert euro_vers_fcfa(100) == 65595.7, "vérifie l'arrondi"

    for montant in [10_000, 50_000, 250_000, 1_000_000]:
        print(afficher(montant))

    print("\n✅ Tous les tests passent.")

# 🛠️ À toi de jouer :
# 1. Ajoute une fonction `prix_au_kilo(montant_total, poids_kg)` qui renvoie le
#    prix au kilo en FCFA, arrondi à l'entier.
# 2. Ajoute la conversion inverse en une phrase lisible (euro → FCFA).
# 3. Enregistre tes modifications :
#       git add .
#       git commit -m "feat: ajoute le prix au kilo et le sens inverse"
#       git push

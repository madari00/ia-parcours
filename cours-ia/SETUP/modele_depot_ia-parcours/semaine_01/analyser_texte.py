"""Semaine 1 — Exercice 2 : analyse de texte (mots les plus fréquents).

À COMPLÉTER : les parties marquées "TODO" sont à écrire par toi.
"""


def compter_mots(texte: str) -> dict[str, int]:
    """Renvoie un dictionnaire {mot: nombre d'occurrences}, en minuscules."""
    mots = texte.lower().split()
    # TODO : construis le dictionnaire. Indice :
    #   compteur = {}
    #   for mot in mots:
    #       compteur[mot] = compteur.get(mot, 0) + 1
    ...


def mots_frequents(texte: str, n: int = 3) -> list[tuple[str, int]]:
    """Renvoie les n mots les plus fréquents, du plus fréquent au moins fréquent."""
    # TODO : utilise sorted() avec key=lambda paire: paire[1], reverse=True
    ...


if __name__ == "__main__":
    texte = (
        "L intelligence artificielle transforme l agriculture au Sahel "
        "L intelligence artificielle aide aussi la sante et l education "
    )
    print("Nombre de mots uniques :", len(compter_mots(texte)))
    for mot, nb in mots_frequents(texte, 3):
        print(f"  {mot:15s} {nb}")

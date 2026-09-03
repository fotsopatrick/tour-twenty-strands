"""Idée 1 — la carte vivante : on regarde avant de réfléchir.

On ne devine jamais le nom d'un champ ou d'un objet Twenty : on interroge
le client une fois, on garde le résultat, et toute recherche ultérieure
relit cette carte au lieu de reparler au réseau.
"""
from datetime import datetime, timezone


def relever(client) -> dict:
    """Lit Twenty via client.lister_objets() et client.compter(objet).

    "entrees" est le nombre d'objets distincts trouvés sur la carte (pas
    la somme de leurs lignes) : c'est ce qui dit si la carte a du contenu.
    """
    objets_champs = client.lister_objets()
    objets = {}
    for nom, champs in objets_champs.items():
        objets[nom] = {"champs": list(champs), "nombre": client.compter(nom)}
    return {
        "date": datetime.now(timezone.utc).isoformat(),
        "objets": objets,
        "entrees": len(objets),
    }


def chercher(carte: dict, mot: str) -> list:
    """Noms d'objets ou de champs contenant `mot`, sans jamais réveiller un modèle."""
    trouves = []
    for nom, info in carte["objets"].items():
        if mot in nom:
            trouves.append(nom)
        for champ in info["champs"]:
            if mot in champ:
                trouves.append(f"{nom}.{champ}")
    return trouves

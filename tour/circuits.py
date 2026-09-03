"""Idée 2 — les circuits : une étape ne monte qu'avec sa preuve.

Une porte refusée arrête tout le chemin : les étapes suivantes ne
s'exécutent jamais. Pas de preuve, pas de passage.
"""
from typing import Callable


class Porte:
    def __init__(self, nom: str, preuve: Callable[[dict], bool]):
        self.nom = nom
        self.preuve = preuve


class Circuit:
    def __init__(self, nom: str, etapes: list):
        self.nom = nom
        self.etapes = etapes

    def executer(self, entree: dict) -> dict:
        etat = entree
        rapport = []
        resultat = None
        for nom_etape, action, porte in self.etapes:
            etat = action(etat)
            ok = bool(porte.preuve(etat))
            rapport.append({"nom": nom_etape, "etat": "passe" if ok else "refuse", "preuve": ok})
            if not ok:
                break
        else:
            resultat = etat
        return {
            "circuit": self.nom,
            "etapes": rapport,
            "resultat": resultat,
            "model_calls": 0,
        }

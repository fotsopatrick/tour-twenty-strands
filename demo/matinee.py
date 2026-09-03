#!/usr/bin/env python3
"""La tournée du matin, jouée en local — sans réseau, sans vrai modèle.

Usage :
    python3 demo/matinee.py

Montre les quatre chemins (rien / relance envoyée / remontée au bureau des
décisions pour cause de garde-fou / remontée pour escalade), un refus de
garde-fou visible, et les compteurs (part de travail fait sans réveiller
le modèle).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tour.agent import Tour
from tour.compteurs import Compteurs
from demo.affaires_inventees import fabriquer, AUJOURDHUI


class DemoTwenty:
    """Un client Twenty minimal pour la démo hors-ligne : range ce qu'on
    lui crée, ne parle à aucun réseau. Même forme que le VraiTwenty."""

    def __init__(self):
        import itertools
        self.tables = {"Decision": {}, "Task": {}}
        self._ids = itertools.count(1)

    def lister_objets(self):
        return {"Opportunity": ["name", "amount", "stage"],
                "Person": ["name", "email"],
                "Decision": ["etat", "brouillon", "raison_machine"]}

    def compter(self, objet):
        return len(self.tables.get(objet, {}))

    def creer(self, objet, data):
        rid = str(next(self._ids))
        self.tables.setdefault(objet, {})[rid] = {"id": rid, **data}
        return self.tables[objet][rid]

    def modifier(self, objet, rid, data):
        self.tables[objet][rid].update(data)
        return self.tables[objet][rid]


class ModeleQuiNeDoitPasSonner:
    """La tournée du matin est entièrement déterministe : si ce modèle est
    appelé, c'est un bug. On le sait tout de suite plutôt que de le
    découvrir en production."""
    appels = 0

    def repondre(self, prompt):
        raise RuntimeError("le modele a ete reveille pendant la tournee du matin — bug")


def main():
    client = DemoTwenty()
    modele = ModeleQuiNeDoitPasSonner()
    regles = {"jours_dormant": 14, "jours_relance_2": 28, "jours_cloture": 60,
              "mots_litige": ["litige", "avocat", "refus"]}
    gabarits = {"relance_1": "Bonjour {nom_contact}, un mot sur {nom_affaire} ?",
                "relance_2": "Bonjour {nom_contact}, je reviens vers vous sur {nom_affaire}."}
    contexte = {"seuil_montant": 5000, "relances_du_jour": 0, "max_relances_jour": 20,
                "delai_min_jours": 7,
                "derniere_relance_contact": {"coline": 2, "elio": 2, "suzy": 2}}

    tour = Tour(client, modele, regles, gabarits, Compteurs())
    affaires = fabriquer()

    print(f"Tournée du matin — {AUJOURDHUI.isoformat()} — {len(affaires)} affaires\n")
    resultat = tour.tournee_du_matin(affaires, AUJOURDHUI, contexte)
    print("Résultat :", resultat)
    print()
    print("Ce que le gardien a réellement refusé (visible, comme demandé) :")
    for rid, d in client.tables["Decision"].items():
        print(f"  Décision {rid} — {d['raison_machine']} — brouillon : {d['brouillon'][:60]}")
    print()
    print("Compteurs :", tour.compteurs.snapshot())
    print()
    print("Preuve que le gardien dit non de la même façon à chaque fois "
          "(même entrée, même verdict) :")
    from tour import gardefous
    args = {"confirm": True, "montant": 9000, "contact": "zzz"}
    print("  ", gardefous.verdict("envoyer_relance", args, contexte))
    print("  ", gardefous.verdict("envoyer_relance", args, contexte))


if __name__ == "__main__":
    main()

"""30 affaires inventees, aucune vraie personne (regle de PROMPT-SIMPLE.md).

Sert a la demo hors-ligne (jeu.py) : varie exprès les cas pour montrer les
quatre chemins (rien / relance_1 / relance_2 / proposer_cloture / escalade)
et deux refus de garde-fou (montant trop haut, relance trop rapprochee).
"""
from datetime import date, timedelta

AUJOURDHUI = date(2026, 9, 3)

_PRENOMS = ["Léa", "Max", "Ana", "Tom", "Zoé", "Iris", "Théo", "Nina",
            "Ali", "Eva", "Noé", "Lou", "Sam", "Rita", "Léo", "Mila",
            "Yann", "Coline", "Elio", "Suzy", "Malo", "Jade", "Timo",
            "Rose", "Igor", "Fanny", "Dan", "Vera", "Kim", "Otto"]


def _jours(n):
    return AUJOURDHUI - timedelta(days=n)


def fabriquer() -> list:
    affaires = []
    for i, prenom in enumerate(_PRENOMS):
        aid = str(i + 1)
        nom_affaire = f"Dossier {aid}"
        contact = prenom.lower()

        if i < 8:  # trop récentes : rien à faire
            affaires.append(dict(id=aid, montant=1200 + i * 50, derniere_activite=_jours(2 + i),
                                  relances=0, contact_a_repondu=False, notes=[],
                                  nom_contact=prenom, nom_affaire=nom_affaire, contact=contact))
        elif i < 14:  # dorment depuis 15-20 jours, petite affaire → relance_1 (envoyée)
            affaires.append(dict(id=aid, montant=800 + i * 30, derniere_activite=_jours(15 + i),
                                  relances=0, contact_a_repondu=False, notes=[],
                                  nom_contact=prenom, nom_affaire=nom_affaire, contact=contact))
        elif i < 17:  # grosse affaire, dort → relance_1 mais refusée (montant)
            affaires.append(dict(id=aid, montant=8000 + i * 100, derniere_activite=_jours(16),
                                  relances=0, contact_a_repondu=False, notes=[],
                                  nom_contact=prenom, nom_affaire=nom_affaire, contact=contact))
        elif i < 20:  # déjà relancée récemment → relance_1 refusée (trop rapproché)
            affaires.append(dict(id=aid, montant=900, derniere_activite=_jours(16),
                                  relances=0, contact_a_repondu=False, notes=[],
                                  nom_contact=prenom, nom_affaire=nom_affaire, contact=contact))
        elif i < 23:  # deuxième relance
            affaires.append(dict(id=aid, montant=1500, derniere_activite=_jours(30),
                                  relances=1, contact_a_repondu=False, notes=[],
                                  nom_contact=prenom, nom_affaire=nom_affaire, contact=contact))
        elif i < 26:  # dort depuis longtemps → proposer clôture
            affaires.append(dict(id=aid, montant=1100, derniere_activite=_jours(65),
                                  relances=2, contact_a_repondu=False, notes=[],
                                  nom_contact=prenom, nom_affaire=nom_affaire, contact=contact))
        elif i < 28:  # le client a répondu → escalade
            affaires.append(dict(id=aid, montant=2000, derniere_activite=_jours(20),
                                  relances=0, contact_a_repondu=True, notes=[],
                                  nom_contact=prenom, nom_affaire=nom_affaire, contact=contact))
        else:  # mot de litige dans les notes → escalade
            affaires.append(dict(id=aid, montant=3000, derniere_activite=_jours(20),
                                  relances=0, contact_a_repondu=False,
                                  notes=["Le client parle d'avocat."],
                                  nom_contact=prenom, nom_affaire=nom_affaire, contact=contact))
    return affaires

"""L'agent — bout en bout, sans réseau, sans vrai modèle."""
from datetime import date, timedelta
from tour.agent import Tour
from tour.compteurs import Compteurs

AUJ = date(2026, 9, 3)


def tour(client, modele, regles, gabarits):
    return Tour(client, modele, regles, gabarits, Compteurs())


def test_capacite_connue_zero_modele(client, modele, regles, gabarits, contexte):
    t = tour(client, modele, regles, gabarits)
    r = t.executer_capacite("lire_carte", {}, contexte)
    assert r["model_calls"] == 0 and modele.appels == 0
    assert t.compteurs.sans_modele == 1


def test_capacite_refusee(client, modele, regles, gabarits, contexte):
    t = tour(client, modele, regles, gabarits)
    r = t.executer_capacite("supprimer_affaire", {"confirm": True}, contexte)
    assert r["decision"] == "REFUSE" and modele.appels == 0
    assert t.compteurs.refus == 1


def test_capacite_inconnue_appelle_le_modele_une_fois(client, modele, regles, gabarits, contexte):
    t = tour(client, modele, regles, gabarits)
    r = t.executer_capacite("envoyer_facture", {"confirm": True}, contexte)
    assert r["model_calls"] == 1 and modele.appels == 1
    assert t.compteurs.avec_modele == 1


def test_tournee_du_matin(client, modele, regles, gabarits, contexte):
    t = tour(client, modele, regles, gabarits)
    affaires = [
        {"id": "a", "montant": 1000, "derniere_activite": AUJ - timedelta(days=15), "relances": 0,
         "contact_a_repondu": False, "notes": [], "nom_contact": "Léa", "nom_affaire": "A", "contact": "lea"},
        {"id": "b", "montant": 9000, "derniere_activite": AUJ - timedelta(days=15), "relances": 0,
         "contact_a_repondu": False, "notes": [], "nom_contact": "Max", "nom_affaire": "B", "contact": "max"},
        {"id": "c", "montant": 500, "derniere_activite": AUJ - timedelta(days=15), "relances": 0,
         "contact_a_repondu": True, "notes": [], "nom_contact": "Ana", "nom_affaire": "C", "contact": "ana"},
        {"id": "d", "montant": 500, "derniere_activite": AUJ - timedelta(days=2), "relances": 0,
         "contact_a_repondu": False, "notes": [], "nom_contact": "Tom", "nom_affaire": "D", "contact": "tom"},
    ]
    r = t.tournee_du_matin(affaires, AUJ, contexte)
    assert r == {"envoyees": 1, "remontees": 2, "rien": 1}
    assert modele.appels == 0
    assert len(client.tables["Decision"]) == 2
    raisons = {d["raison_machine"] for d in client.tables["Decision"].values()}
    assert "montant au-dessus du seuil" in raisons
    assert t.compteurs.decisions_remontees == 2

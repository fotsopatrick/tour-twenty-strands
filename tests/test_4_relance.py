"""Le scénario — classer une affaire qui dort, sans modèle."""
from datetime import date, timedelta
from tour import relance


def affaire(**k):
    base = {"id": "1", "montant": 1000, "derniere_activite": date(2026, 9, 1),
            "relances": 0, "contact_a_repondu": False, "notes": [],
            "nom_contact": "Léa", "nom_affaire": "Site vitrine"}
    base.update(k)
    return base


AUJ = date(2026, 9, 3)


def test_rien_si_recente(regles):
    assert relance.classer(affaire(), AUJ, regles) == "rien"


def test_relance_1(regles):
    a = affaire(derniere_activite=AUJ - timedelta(days=15))
    assert relance.classer(a, AUJ, regles) == "relance_1"


def test_relance_2(regles):
    a = affaire(derniere_activite=AUJ - timedelta(days=30), relances=1)
    assert relance.classer(a, AUJ, regles) == "relance_2"


def test_proposer_cloture(regles):
    a = affaire(derniere_activite=AUJ - timedelta(days=61), relances=2)
    assert relance.classer(a, AUJ, regles) == "proposer_cloture"


def test_escalade_si_repondu(regles):
    a = affaire(derniere_activite=AUJ - timedelta(days=20), contact_a_repondu=True)
    assert relance.classer(a, AUJ, regles) == "escalade"


def test_escalade_si_litige(regles):
    a = affaire(derniere_activite=AUJ - timedelta(days=20), notes=["Le client parle d'avocat"])
    assert relance.classer(a, AUJ, regles) == "escalade"


def test_brouillon_sans_modele(gabarits):
    b = relance.brouillon(affaire(), "relance_1", gabarits)
    assert b == "Bonjour Léa, un mot sur Site vitrine ?"

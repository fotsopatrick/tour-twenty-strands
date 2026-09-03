"""Idée 4 — le bureau des décisions : refuser sans raison est interdit."""
import pytest
from tour import decisions


def test_remonter_cree_une_decision_en_attente(client):
    d = decisions.remonter(client, "42", "Bonjour…", "montant au-dessus du seuil")
    assert d["etat"] == "en_attente"
    assert d["verdict_machine"] == "REFUSE"
    assert d["raison_machine"] == "montant au-dessus du seuil"
    assert client.journal[-1][0] == "creer" and client.journal[-1][1] == "Decision"


def test_refus_sans_raison_bloque(client):
    d = decisions.remonter(client, "42", "x", "r")
    with pytest.raises(decisions.RaisonManquante):
        decisions.trancher(client, d["id"], "refuse", "   ")
    assert client.tables["Decision"][d["id"]]["etat"] == "en_attente"
    assert not any(a[0] == "modifier" for a in client.journal)


def test_refus_avec_raison(client):
    d = decisions.remonter(client, "42", "x", "r")
    r = decisions.trancher(client, d["id"], "refuse", "trop tôt, le client est en congé")
    assert r["etat"] == "refuse" and r["raison_humaine"].startswith("trop tôt")


def test_approbation(client):
    d = decisions.remonter(client, "42", "x", "r")
    r = decisions.trancher(client, d["id"], "approuve", "")
    assert r["etat"] == "approuve"

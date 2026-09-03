"""Idée 1 — la carte vivante : on regarde avant de réfléchir."""
from tour import carte


def test_relever_lit_twenty_et_compte(client):
    c = carte.relever(client)
    assert "Opportunity" in c["objets"]
    assert c["objets"]["Opportunity"]["champs"] == ["name", "amount", "stage"]
    assert c["entrees"] >= 3
    assert ("lister_objets",) in client.journal


def test_chercher_sans_modele(client):
    c = carte.relever(client)
    trouves = carte.chercher(c, "amount")
    assert any("amount" in t for t in trouves)
    assert carte.chercher(c, "zzz") == []

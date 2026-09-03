"""Idée 3 — les garde-fous : même entrée, même verdict, toujours."""
from tour import gardefous as g


def test_liste_noire(contexte):
    ok, raison = g.verdict("supprimer_affaire", {"confirm": True}, contexte)
    assert ok is False and raison == "liste noire"


def test_ecriture_sans_confirm(contexte):
    ok, raison = g.verdict("creer_tache", {}, contexte)
    assert ok is False and raison == "confirm requis"


def test_ecriture_avec_confirm(contexte):
    ok, _ = g.verdict("creer_tache", {"confirm": True}, contexte)
    assert ok is True


def test_montant_au_dessus_du_seuil(contexte):
    ok, raison = g.verdict("envoyer_relance", {"confirm": True, "montant": 9000, "contact": "a"}, contexte)
    assert ok is False and raison == "montant au-dessus du seuil"


def test_quota_du_jour(contexte):
    contexte["relances_du_jour"] = 20
    ok, raison = g.verdict("envoyer_relance", {"confirm": True, "montant": 100, "contact": "a"}, contexte)
    assert ok is False and raison == "quota du jour atteint"


def test_relance_trop_rapprochee(contexte):
    contexte["derniere_relance_contact"] = {"a": 2}  # relancé il y a 2 jours
    ok, raison = g.verdict("envoyer_relance", {"confirm": True, "montant": 100, "contact": "a"}, contexte)
    assert ok is False and raison == "relance trop rapprochee"


def test_deterministe(contexte):
    args = {"confirm": True, "montant": 100, "contact": "b"}
    r1 = g.verdict("envoyer_relance", args, contexte)
    r2 = g.verdict("envoyer_relance", args, contexte)
    assert r1 == r2 == (True, "ok")

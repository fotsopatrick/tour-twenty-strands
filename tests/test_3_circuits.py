"""Idée 2 — les circuits : une étape ne monte qu'avec sa preuve."""
from tour.circuits import Circuit, Porte


def test_chemin_vert():
    c = Circuit("compte", [
        ("ajoute", lambda e: {**e, "x": e["x"] + 1}, Porte("x est 2", lambda s: s["x"] == 2)),
        ("double", lambda e: {**e, "x": e["x"] * 2}, Porte("x est 4", lambda s: s["x"] == 4)),
    ])
    r = c.executer({"x": 1})
    assert [e["etat"] for e in r["etapes"]] == ["passe", "passe"]
    assert r["resultat"]["x"] == 4
    assert r["model_calls"] == 0


def test_rebond_rouge_arrete_le_circuit():
    appels = []
    c = Circuit("casse", [
        ("etape1", lambda e: e, Porte("toujours non", lambda s: False)),
        ("etape2", lambda e: appels.append("etape2") or e, Porte("oui", lambda s: True)),
    ])
    r = c.executer({})
    assert r["etapes"][0]["etat"] == "refuse"
    assert len(r["etapes"]) == 1
    assert appels == []
    assert r["resultat"] is None

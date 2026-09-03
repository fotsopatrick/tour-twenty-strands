"""Observabilité — la mesure, pas la phrase."""
from tour.compteurs import Compteurs


def test_part_sans_modele():
    c = Compteurs()
    assert c.snapshot()["part_sans_modele"] == 0
    for _ in range(19):
        c.sans_modele += 1
    c.avec_modele += 1
    assert c.snapshot()["part_sans_modele"] == 95.0

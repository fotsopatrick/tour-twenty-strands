"""Observabilité — la mesure, pas la phrase."""


class Compteurs:
    def __init__(self):
        self.sans_modele = 0
        self.avec_modele = 0
        self.refus = 0
        self.decisions_remontees = 0
        self.decisions_refusees = 0

    def snapshot(self) -> dict:
        total = self.sans_modele + self.avec_modele
        part = (self.sans_modele / total * 100) if total else 0
        return {
            "sans_modele": self.sans_modele,
            "avec_modele": self.avec_modele,
            "refus": self.refus,
            "decisions_remontees": self.decisions_remontees,
            "decisions_refusees": self.decisions_refusees,
            "part_sans_modele": part,
        }

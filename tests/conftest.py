import itertools
import pytest


class FauxTwenty:
    def __init__(self):
        self.journal = []
        self.tables = {"Decision": {}, "Opportunity": {}, "Task": {}}
        self._ids = itertools.count(1)

    def lister_objets(self):
        self.journal.append(("lister_objets",))
        return {"Opportunity": ["name", "amount", "stage"],
                "Person": ["name", "email"],
                "Decision": ["etat", "brouillon", "raison_machine"]}

    def compter(self, objet):
        self.journal.append(("compter", objet))
        return len(self.tables.get(objet, {}))

    def creer(self, objet, data):
        self.journal.append(("creer", objet, dict(data)))
        rid = str(next(self._ids))
        self.tables.setdefault(objet, {})[rid] = {"id": rid, **data}
        return self.tables[objet][rid]

    def modifier(self, objet, rid, data):
        self.journal.append(("modifier", objet, rid, dict(data)))
        self.tables[objet][rid].update(data)
        return self.tables[objet][rid]


class FauxModele:
    def __init__(self):
        self.appels = 0

    def repondre(self, prompt):
        self.appels += 1
        return "reponse du modele"


@pytest.fixture
def client():
    return FauxTwenty()


@pytest.fixture
def modele():
    return FauxModele()


@pytest.fixture
def regles():
    return {"jours_dormant": 14, "jours_relance_2": 28, "jours_cloture": 60,
            "mots_litige": ["litige", "avocat", "refus"]}


@pytest.fixture
def gabarits():
    return {"relance_1": "Bonjour {nom_contact}, un mot sur {nom_affaire} ?",
            "relance_2": "Bonjour {nom_contact}, je reviens vers vous sur {nom_affaire}."}


@pytest.fixture
def contexte():
    return {"seuil_montant": 5000, "relances_du_jour": 0, "max_relances_jour": 20,
            "delai_min_jours": 7, "derniere_relance_contact": {}}

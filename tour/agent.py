"""L'agent — le cerveau intelligent n'est réveillé que si personne d'autre
ne sait répondre.
"""
from . import carte, decisions, gardefous


def _lire_carte(tour, args, contexte):
    return carte.relever(tour.client)


class Tour:
    # Capacités connues : exécutées sans jamais réveiller le modèle.
    CAPACITES = {
        "lire_carte": _lire_carte,
    }

    def __init__(self, client, modele, regles, gabarits, compteurs):
        self.client = client
        self.modele = modele
        self.regles = regles
        self.gabarits = gabarits
        self.compteurs = compteurs

    def executer_capacite(self, nom: str, args: dict, contexte: dict) -> dict:
        ok, raison = gardefous.verdict(nom, args, contexte)
        if not ok:
            self.compteurs.refus += 1
            return {"decision": "REFUSE", "raison": raison, "model_calls": 0}

        gestionnaire = self.CAPACITES.get(nom)
        if gestionnaire is not None:
            resultat = gestionnaire(self, args, contexte)
            self.compteurs.sans_modele += 1
            return {"decision": "OK", "resultat": resultat, "model_calls": 0}

        prompt = "Capacite inconnue : %s\nArgs : %r" % (nom, args)
        reponse = self.modele.repondre(prompt)
        self.compteurs.avec_modele += 1
        return {"decision": "MODELE", "reponse": reponse, "model_calls": 1}

    def tournee_du_matin(self, affaires: list, aujourd_hui, contexte: dict) -> dict:
        """Chaque matin : classer les affaires qui dorment, envoyer ce que le
        garde-fou autorise, remonter le reste au bureau des décisions —
        jamais un modèle réveillé pour ce travail."""
        from tour import relance

        envoyees = remontees = rien = 0
        for affaire in affaires:
            classement = relance.classer(affaire, aujourd_hui, self.regles)

            if classement == "rien":
                rien += 1
                continue

            if classement in ("relance_1", "relance_2"):
                texte = relance.brouillon(affaire, classement, self.gabarits)
                args = {
                    "confirm": True,
                    "montant": affaire["montant"],
                    "contact": affaire.get("contact", affaire["id"]),
                }
                ok, raison = gardefous.verdict("envoyer_relance", args, contexte)
                if ok:
                    self.client.creer("Task", {
                        "affaire_id": affaire["id"], "type": classement, "corps": texte,
                    })
                    envoyees += 1
                    continue
            else:
                # escalade / proposer_cloture : jamais envoyé seul.
                texte = "(%s) %s — %s" % (classement, affaire["nom_contact"], affaire["nom_affaire"])
                raison = classement

            decisions.remonter(self.client, affaire["id"], texte, raison)
            self.compteurs.decisions_remontees += 1
            remontees += 1

        return {"envoyees": envoyees, "remontees": remontees, "rien": rien}

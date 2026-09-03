"""Le scénario — classer une affaire qui dort, sans réveiller un modèle."""
from datetime import date


def classer(affaire: dict, aujourd_hui: date, regles: dict) -> str:
    if affaire["contact_a_repondu"]:
        return "escalade"
    mots_litige = [m.lower() for m in regles["mots_litige"]]
    for note in affaire["notes"]:
        if any(mot in note.lower() for mot in mots_litige):
            return "escalade"

    dormant = (aujourd_hui - affaire["derniere_activite"]).days

    if dormant >= regles["jours_cloture"]:
        return "proposer_cloture"
    if dormant >= regles["jours_relance_2"] and affaire["relances"] == 1:
        return "relance_2"
    if dormant >= regles["jours_dormant"] and affaire["relances"] == 0:
        return "relance_1"
    return "rien"


def brouillon(affaire: dict, niveau: str, gabarits: dict) -> str:
    return gabarits[niveau].format(
        nom_contact=affaire["nom_contact"], nom_affaire=affaire["nom_affaire"]
    )

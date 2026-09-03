"""Idée 4 — le bureau des décisions : refuser sans raison est interdit."""


class RaisonManquante(Exception):
    pass


def remonter(client, affaire_id, brouillon, raison_machine) -> dict:
    return client.creer("Decision", {
        "affaire_id": affaire_id,
        "brouillon": brouillon,
        "raison_machine": raison_machine,
        "etat": "en_attente",
        "verdict_machine": "REFUSE",
        "verdict_humain": None,
        "raison_humaine": None,
    })


def trancher(client, decision_id, verdict: str, raison: str) -> dict:
    if verdict == "refuse" and raison.strip() == "":
        raise RaisonManquante("un refus doit toujours porter une raison")
    return client.modifier("Decision", decision_id, {
        "etat": verdict,
        "verdict_humain": verdict,
        "raison_humaine": raison,
    })

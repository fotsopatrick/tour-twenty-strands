"""Idée 3 — les garde-fous : même entrée, même verdict, toujours.

Aucune horloge, aucun aléa, aucun réseau ici : verdict() est une fonction
pure. Un gardien qui ne dit jamais non ne garde rien — la démo doit
pouvoir montrer un refus.
"""

LISTE_NOIRE = {"supprimer_affaire", "exporter_tout", "supprimer_contact"}

PREFIXES_ECRITURE = ("creer_", "envoyer_", "modifier_")


def verdict(capacite: str, args: dict, contexte: dict):
    if capacite in LISTE_NOIRE:
        return False, "liste noire"

    if capacite.startswith(PREFIXES_ECRITURE) and args.get("confirm") is not True:
        return False, "confirm requis"

    if capacite == "envoyer_relance":
        if args.get("montant", 0) > contexte["seuil_montant"]:
            return False, "montant au-dessus du seuil"
        if contexte.get("relances_du_jour", 0) >= contexte["max_relances_jour"]:
            return False, "quota du jour atteint"
        derniers = contexte.get("derniere_relance_contact", {})
        contact = args.get("contact")
        if contact in derniers and derniers[contact] < contexte["delai_min_jours"]:
            return False, "relance trop rapprochee"

    return True, "ok"

# Contrat de code — ce que les tests attendent

Les tests ci-dessous ne parlent jamais à Twenty ni à un modèle : ils reçoivent un faux client
(`FauxTwenty`) et un faux modèle (`FauxModele`). Le vrai client Twenty et le vrai appel Strands
doivent respecter exactement ces interfaces. Ce contrat est la seule chose que le code doit tenir.

Paquet : `tour/`

## tour/carte.py
- `relever(client) -> dict` : lit Twenty via `client.lister_objets()` et `client.compter(objet)`,
  renvoie `{"date": iso, "objets": {nom: {"champs": [...], "nombre": int}}, "entrees": int}`.
- `chercher(carte, mot) -> list[str]` : noms d'objets ou de champs contenant `mot`, sans modèle.

## tour/gardefous.py
- `LISTE_NOIRE = {"supprimer_affaire", "exporter_tout", "supprimer_contact"}`
- `verdict(capacite, args, contexte) -> (bool, str)`
  - capacité dans LISTE_NOIRE → `(False, "liste noire")`
  - capacité qui écrit (préfixe `creer_`, `envoyer_`, `modifier_`) sans `args["confirm"] is True` → `(False, "confirm requis")`
  - `envoyer_relance` avec `args["montant"] > contexte["seuil_montant"]` → `(False, "montant au-dessus du seuil")`
  - `envoyer_relance` si `contexte["relances_du_jour"] >= contexte["max_relances_jour"]` → `(False, "quota du jour atteint")`
  - `envoyer_relance` si le contact a été relancé il y a moins de `contexte["delai_min_jours"]` → `(False, "relance trop rapprochee")`
  - sinon `(True, "ok")`
- Même entrée, même sortie : aucune horloge, aucun aléa, aucun réseau dans ce fichier.

## tour/circuits.py
- `class Porte(nom, preuve: Callable[[dict], bool])`
- `class Circuit(nom, etapes: list[(nom_etape, action: Callable[[dict], dict], porte: Porte)])`
- `Circuit.executer(entree: dict) -> dict` renvoie
  `{"circuit": nom, "etapes": [{"nom", "etat": "passe"|"refuse", "preuve": bool}], "resultat": dict|None, "model_calls": 0}`.
  Une étape refusée arrête le circuit ; les étapes suivantes ne sont pas exécutées.

## tour/relance.py
- `classer(affaire: dict, aujourd_hui: date, regles: dict) -> str`
  parmi `"rien"`, `"relance_1"`, `"relance_2"`, `"proposer_cloture"`, `"escalade"`.
  - `affaire = {"id", "montant", "derniere_activite": date, "relances": int, "contact_a_repondu": bool, "notes": [str]}`
  - `regles = {"jours_dormant": 14, "jours_relance_2": 28, "jours_cloture": 60, "mots_litige": ["litige","avocat","refus"]}`
  - contact a répondu → `"escalade"` ; un mot de litige dans les notes → `"escalade"` ;
    dormant depuis ≥ jours_cloture → `"proposer_cloture"` ; dormant ≥ jours_relance_2 et relances==1 → `"relance_2"` ;
    dormant ≥ jours_dormant et relances==0 → `"relance_1"` ; sinon `"rien"`.
- `brouillon(affaire, niveau, gabarits: dict) -> str` : remplit `gabarits[niveau]` avec `{nom_contact}`, `{nom_affaire}` ; ne touche à aucun modèle.

## tour/decisions.py
- `remonter(client, affaire_id, brouillon, raison_machine) -> dict` : crée via `client.creer("Decision", {...})`
  avec `etat="en_attente"`, `verdict_machine="REFUSE"`, `raison_machine=raison_machine`.
- `trancher(client, decision_id, verdict: "approuve"|"refuse", raison: str) -> dict`
  - `verdict == "refuse"` et `raison.strip() == ""` → lève `RaisonManquante` et ne modifie rien.
  - sinon `client.modifier("Decision", id, {"etat": verdict, "verdict_humain": verdict, "raison_humaine": raison})`.

## tour/compteurs.py
- `Compteurs` avec `.sans_modele`, `.avec_modele`, `.refus`, `.decisions_remontees`, `.decisions_refusees`
  et `.snapshot() -> dict` avec en plus `"part_sans_modele"` en pourcentage (0 si rien).

## tour/agent.py
- `Tour(client, modele, regles, gabarits, compteurs)`
- `Tour.executer_capacite(nom, args, contexte) -> dict` : passe par `gardefous.verdict` d'abord ;
  refus → `{"decision": "REFUSE", "raison": ..., "model_calls": 0}` + compteurs.refus += 1 ;
  capacité connue (dans `Tour.CAPACITES`) → exécutée, `model_calls: 0`, compteurs.sans_modele += 1 ;
  inconnue → `modele.repondre(prompt)`, `model_calls: 1`, compteurs.avec_modele += 1.
- `Tour.tournee_du_matin(affaires, aujourd_hui, contexte) -> dict` : applique `classer` à chaque affaire,
  envoie seule les relances autorisées par le garde-fou, remonte une Décision pour tout le reste
  (escalade, clôture, ou relance refusée par le garde-fou). Renvoie `{"envoyees": n, "remontees": n, "rien": n}`.

## Faux objets fournis par tests/conftest.py
- `FauxTwenty` : `lister_objets()`, `compter(objet)`, `creer(objet, data) -> dict avec id`, `modifier(objet, id, data)`,
  `journal` = liste de tous les appels.
- `FauxModele` : `repondre(prompt) -> "reponse du modele"`, `.appels` = nombre d'appels.

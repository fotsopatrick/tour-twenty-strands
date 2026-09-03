# Limites — ce qu'on ne sait pas encore faire

Écrit le 03/09/2026, à la fin de la première session de construction.

## Vérifié, qui marche

- Les 27 tests du contrat passent contre de faux objets (`pytest -q`).
- La tournée du matin tourne de bout en bout en local, sans réseau, sur
  30 affaires inventées (`demo/matinee.py`) : 9 relances envoyées seules,
  13 questions remontées, 8 rien à faire, le modèle jamais réveillé.
- Twenty (CRM) tourne en local dans Docker, avec les fichiers officiels du
  projet (`twenty-local/`), et répond sur `http://localhost:3000`.
- Le SDK Strands est installé (`strands-agents`, Apache 2.0) et sait
  répondre à un prompt simple selon sa documentation (non rejoué en
  direct — voir plus bas).

## PAS VÉRIFIÉ — à confirmer avec une vraie clé Twenty

`tour/twenty_client.py` (VraiTwenty) est écrit d'après la documentation
publique de Twenty, mais jamais rejoué contre un vrai compte : le premier
compte de ce Twenty local n'a pas encore été créé au moment où ce fichier
est écrit (créer un compte et choisir un mot de passe est un geste que
l'assistant ne fait jamais à la place de quelqu'un, même en local — il
attend Patrick).

Une fois une clé disponible (`Réglages > API et Webhooks` dans Twenty) :
- `lister_objets()` : Twenty n'expose pas d'un coup « tous les objets et
  leurs champs » en REST simple. Le geste actuel interroge quelques objets
  connus un par un et lit les champs du premier enregistrement — à
  vérifier, et probablement à remplacer par l'API GraphQL de métadonnées.
- `compter(objet)` : suppose un champ `totalCount` dans la réponse — à
  confirmer.
- `tests/test_8_twenty_reel.py` (marqué `reseau`, prévu par le contrat) :
  pas encore écrit, en attente de la clé.

## PAS VÉRIFIÉ — le vrai modèle

`tour/strands_agent.py` (ModeleStrands) est écrit d'après la documentation
Strands, mais jamais appelé pour de vrai : aucun identifiant de modèle
(compte Amazon Bedrock, ou clé Anthropic / OpenAI directe) n'est configuré
sur ce poste. `tests/test_9_strands_reel.py` (marqué `reseau`) n'est pas
encore écrit.

## Pas commencé

- **AgentCore (Amazon)** : le robot tourne en Docker local, pas encore
  chez Amazon. À faire si le temps le permet (jour 8 du plan).
- **Vidéo de 5 minutes**, **dessin de la maison**, **article
  builder.aws.com** : pas encore faits.
- **Dépôt public** : le code est encore seulement sur ce poste.
- **Boîtes Twenty « Décision », « Chemin exécuté », « Alerte du gardien »** :
  seule « Decision » est créée par le code pour l'instant ; les deux
  autres ne sont pas encore posées dans Twenty.

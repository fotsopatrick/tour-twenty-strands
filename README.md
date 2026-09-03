# Tour — un robot qui aide une personne qui vend des choses

Construit pour le concours **Agents for Humans Hackathon** (AWS / Strands).

📋 **[La présentation en une page](https://claude.ai/code/artifact/bfcd36a0-a7c5-40c6-9d05-c45fabf9d537)** — le pitch, le schéma du circuit, les chiffres mesurés.

## Le problème, en une phrase

Chaque matin, des affaires dorment dans le CRM parce que personne n'a eu le
temps de relancer le client. Un robot peut le faire — mais un robot qui
envoie n'importe quoi, n'importe quand, à n'importe qui, fait plus de mal
que de bien.

## Pour qui

Une personne seule qui vend, avec un CRM [Twenty](https://twenty.com) et
peu de temps pour le surveiller.

## Comment ça marche

Chaque matin, le robot regarde les affaires qui dorment (via
[Twenty](https://twenty.com), licence AGPLv3 avec une exception explicite
pour les applications qui ne parlent que par son API — voir son
[LICENSE](https://github.com/twentyhq/twenty/blob/main/LICENSE) — ce qui
autorise ce robot, sous licence MIT, à s'y brancher) :

- **petite affaire, première fois qui dort** → un mot gentil part tout
  seul, écrit à l'avance dans un gabarit ;
- **grosse affaire, client qui a répondu, ou mot de litige dans les
  notes** → rien ne part ; une question est posée à la personne, avec le
  mot déjà écrit et la raison de l'arrêt.

Quatre règles tiennent tout ça :

1. **La carte** (`tour/carte.py`) : le robot lit d'abord ce qui existe dans
   Twenty, il ne le devine jamais.
2. **Les chemins avec des portes** (`tour/circuits.py`) : chaque travail est
   une suite d'étapes, chacune avec sa preuve. Pas de preuve, le chemin
   s'arrête là.
3. **Les gardiens** (`tour/gardefous.py`) : liste noire, confirmation
   obligatoire pour écrire, seuil de montant, quota du jour, délai minimum
   entre deux relances au même contact. Le refus est déterministe : même
   entrée, même verdict, toujours (`tests/test_2_gardefous.py`).
4. **La table des questions** (`tour/decisions.py`) : tout ce qu'un gardien
   arrête devient une Décision dans Twenty. Refuser sans dire pourquoi est
   impossible : le code lève une erreur (`RaisonManquante`).

Le grand modèle ([Strands](https://strandsagents.com), licence Apache 2.0)
n'est réveillé que si aucune des capacités connues du robot ne sait
répondre (`tour/agent.py`, `Tour.executer_capacite`). Deux compteurs
existent pour le prouver : combien de fois le robot a réussi seul, combien
de fois il a réveillé le modèle (`tour/compteurs.py`).

## Installer et essayer en 15 minutes

```bash
# 1. l'environnement Python
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# 2. la logique, sans rien d'externe (27 tests)
.venv/bin/pytest -q
# -> 27 passed

# 3. la démo hors-ligne : une tournée du matin, 30 affaires inventées
.venv/bin/python3 demo/matinee.py

# 4. Twenty en local (Docker)
cd twenty-local && docker compose up -d
# -> http://localhost:3000, créer le premier compte, puis
#    Réglages > API et Webhooks > + Créer une clé
export TWENTY_API_KEY=<la clé>
```

## Chiffres mesurés (démo hors-ligne, 30 affaires inventées)

| | |
|---|---|
| Relances envoyées seules | 9 |
| Remontées à la personne (question posée) | 13 |
| Rien à faire | 8 |
| Modèle réveillé | 0 fois |

## Où le robot tourne

En Docker en local pour l'instant (voir `twenty-local/`). Le portage vers
Amazon Bedrock AgentCore n'est pas encore fait — voir `LIMITES.md`.

## Structure

```
tour/               le robot (aucune dépendance à Twenty ou Strands sauf
                     twenty_client.py et strands_agent.py)
tests/               27 tests, fournis avec le concours, contre de faux
                     objets (aucun réseau)
demo/                la tournée du matin jouée hors-ligne, avec 30 affaires
                     inventées, aucune vraie personne
twenty-local/        Twenty CRM, fichiers officiels de docker-compose
CONTRAT.md           le contrat que le code doit tenir
PROMPT-SIMPLE.md     le cahier des charges, dit simplement
LIMITES.md           ce qu'on ne sait pas encore faire
```

## Licence

MIT (voir `LICENSE`).

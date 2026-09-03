"""Le cerveau intelligent — reveille seulement quand personne d'autre ne
sait repondre (voir tour/agent.py, Tour.executer_capacite).

Doc utilisee : https://strandsagents.com/docs/user-guide/quickstart/python/
Licence Strands : Apache 2.0. Installation : pip install strands-agents.

PAS VERIFIE EN DIRECT : aucun identifiant de modele (Bedrock ou cle
Anthropic/OpenAI) n'est configure sur ce poste au moment ou ce fichier est
ecrit. Voir LIMITES.md.
"""
from strands import Agent


class ModeleStrands:
    """Respecte l'interface que tour/agent.py attend d'un modele :
    .repondre(prompt) -> str, .appels compte les vrais appels."""

    def __init__(self, agent: Agent = None):
        self.agent = agent or Agent()
        self.appels = 0

    def repondre(self, prompt: str) -> str:
        self.appels += 1
        resultat = self.agent(prompt)
        return str(resultat.message)

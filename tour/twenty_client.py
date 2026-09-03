"""Le vrai client Twenty — parle par la porte officielle (l'API REST),
jamais en fouillant dans sa base.

Doc utilisee : https://docs.twenty.com/developers/extend/api (API REST,
authentification "Authorization: Bearer <cle>"). Cle a creer dans Twenty :
Reglages > API et Webhooks > + Creer une cle.

Respecte exactement l'interface que carte.py, decisions.py et agent.py
attendent (voir CONTRAT.md) : lister_objets(), compter(objet),
creer(objet, data), modifier(objet, id, data). Le journal des appels
n'est pas garde ici (ce n'est utile qu'au faux client des tests).
"""
import os
import requests


class VraiTwenty:
    def __init__(self, base_url: str = None, api_key: str = None):
        self.base_url = (base_url or os.environ.get("TWENTY_URL", "http://localhost:3000")).rstrip("/")
        self.api_key = api_key or os.environ.get("TWENTY_API_KEY")
        if not self.api_key:
            raise RuntimeError(
                "TWENTY_API_KEY manquante. Cree une cle dans Twenty : "
                "Reglages > API et Webhooks > + Creer une cle, et exporte-la."
            )
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        })

    # -- Les quatre gestes que le contrat demande --------------------------

    def lister_objets(self) -> dict:
        """PAS VERIFIE EN DIRECT (compte pas encore cree au moment ou ce
        fichier est ecrit) : Twenty n'a pas d'endpoint unique "liste tous
        les objets et leurs champs" en REST simple — la carte complete des
        types passe par l'API GraphQL de metadonnees
        (https://docs.twenty.com/developers/extend/api). Le geste ici
        interroge les objets standards connus un par un via REST et lit
        leurs champs sur le premier enregistrement rendu. A completer /
        verifier une fois une cle reelle disponible.
        """
        objets = {}
        for nom_api in ("opportunities", "people", "tasks"):
            reponse = self.session.get(f"{self.base_url}/rest/{nom_api}", params={"limit": 1})
            reponse.raise_for_status()
            lignes = reponse.json().get("data", {}).get(nom_api, [])
            champs = list(lignes[0].keys()) if lignes else []
            objets[nom_api] = champs
        return objets

    def compter(self, objet: str) -> int:
        reponse = self.session.get(f"{self.base_url}/rest/{objet}", params={"limit": 1})
        reponse.raise_for_status()
        corps = reponse.json()
        # PAS VERIFIE : le nombre total exact suppose une pagination lisible
        # via un total renvoye par l'API ; a confirmer avec une vraie cle.
        return corps.get("totalCount", len(corps.get("data", {}).get(objet, [])))

    def creer(self, objet: str, data: dict) -> dict:
        reponse = self.session.post(f"{self.base_url}/rest/{objet}", json=data)
        reponse.raise_for_status()
        return reponse.json().get("data", {}).get(objet[:-1] if objet.endswith("s") else objet, reponse.json())

    def modifier(self, objet: str, rid: str, data: dict) -> dict:
        reponse = self.session.patch(f"{self.base_url}/rest/{objet}/{rid}", json=data)
        reponse.raise_for_status()
        return reponse.json().get("data", {}).get(objet[:-1] if objet.endswith("s") else objet, reponse.json())

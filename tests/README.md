# Lancer les tests

    pip install pytest
    pytest -q

Tu dois voir : `27 passed`. Tant que ce n'est pas le cas, le code ne respecte pas CONTRAT.md.

Ces tests ne touchent ni Twenty, ni Strands, ni un modèle. Ils prouvent la logique.
Deux tests supplémentaires, à écrire seulement quand l'API est vérifiée dans la doc :

- `tests/test_8_twenty_reel.py` (marqué `@pytest.mark.reseau`) : avec une clé d'API et un espace de démo,
  `carte.relever(VraiTwenty())` renvoie au moins l'objet `Decision` ; `decisions.remonter` crée bien un
  enregistrement visible dans l'interface.
- `tests/test_9_strands_reel.py` (marqué `@pytest.mark.reseau`) : l'agent Strands, face à une capacité
  connue, produit un `model_calls: 0` dans sa trace, et face à une capacité inconnue, exactement 1.

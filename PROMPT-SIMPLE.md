# Le prompt, dit simplement

Tu vas construire un petit robot qui aide une personne qui vend des choses.
Cette personne range ses clients et ses affaires dans un logiciel qui s'appelle Twenty.
Le robot est fait avec Strands, une boîte à outils d'Amazon pour faire des robots.
On a 10 jours. On est seul. On part d'une page blanche.

## Ce que le robot fait

Chaque matin, le robot regarde les affaires qui dorment : personne n'a parlé au client depuis longtemps.

- Si c'est une petite affaire et que c'est la première fois, le robot envoie un petit mot gentil au client tout seul.
- Si c'est une grosse affaire, ou si le client a répondu, ou si le client est fâché, le robot n'envoie rien.
  Il pose la question sur la table de la personne : « je fais ça ? » avec le mot déjà écrit.
- La personne dit oui, ou dit non. Si elle dit non, elle doit dire pourquoi. Un « non » sans pourquoi n'est pas accepté.

La personne ne voit que les questions. Tout le reste, le robot le fait sans la déranger.

## Les quatre règles de la maison

1. **La carte.** Avant de réfléchir, le robot regarde sa carte : la liste de tout ce qui existe dans Twenty. Si la réponse est sur la carte, il ne réfléchit pas, il lit.
2. **Les chemins avec des portes.** Chaque travail est un chemin en plusieurs pas. Entre deux pas, il y a une porte. La porte s'ouvre seulement si on montre une preuve. Pas de preuve, la porte reste fermée, et le travail redescend.
3. **Les gardiens.** Certaines choses sont interdites (effacer, tout envoyer d'un coup, envoyer trop, envoyer deux fois au même client dans la semaine). Le gardien dit non, et il dit non de la même façon à chaque fois. Un gardien qui ne dit jamais non ne garde rien : dans la démo, on doit le voir dire non.
4. **La table des questions.** Tout ce que le gardien a arrêté devient une question pour la personne, rangée dans Twenty, avec le mot déjà écrit et la raison de l'arrêt.

Le cerveau intelligent (le grand modèle) n'est réveillé que si personne d'autre ne sait répondre. On compte à part : combien de fois on a réussi sans le réveiller, combien de fois on l'a réveillé. Ce chiffre s'affiche.

## Ce qu'on ne fait jamais

- On n'invente pas comment marche Strands ou Twenty. On lit leur mode d'emploi, on met le lien dans le code. Si on ne trouve pas, on écrit « PAS VÉRIFIÉ » et on demande.
- On écrit le test avant le code. Chaque règle a son test : un test où la porte s'ouvre, un test où elle reste fermée. Les tests sont déjà écrits dans le dossier `tests/` et le contrat est dans `CONTRAT.md` : le code doit les faire passer tous. Tu dois voir `27 passed`.
- On ne promet rien qu'on n'a pas testé. Ce qu'on ne sait pas faire est écrit dans `LIMITES.md`.
- Pas de vraies personnes dans le dépôt. Des clients inventés seulement.

## Comment on parle à Twenty et à Strands

- Twenty tourne dans Docker avec le fichier fourni par Twenty.
- Le robot parle à Twenty par sa porte officielle (l'API), jamais en fouillant dans sa base.
- Dans Twenty on crée trois boîtes : « Décision », « Chemin exécuté », « Alerte du gardien ».
- Le robot tourne chez Amazon (AgentCore) si on y arrive. Sinon dans une boîte Docker, et on écrit pourquoi.
- Le code du robot est sous licence MIT. On vérifie que la licence de Twenty le permet et on l'écrit.

## Ce qu'on rend

1. Un dépôt public avec un mode d'emploi : le problème, pour qui, comment ça marche, comment l'installer en 15 minutes, les chiffres mesurés.
2. Un dessin de la maison : la demande, le gardien, la carte ou le chemin ou le cerveau, la table des questions, les compteurs.
3. Une vidéo de 5 minutes : le problème, pour qui, pourquoi ça compte, puis le matin qui tourne, un mot qui part tout seul, une question qui arrive, la personne qui dit non avec un pourquoi, les chiffres qui bougent.
4. Un lien pour essayer si possible.
5. Un article sur builder.aws.com avec « Agents for Humans » dans le titre.

## Les jours

- Jour 1 : Twenty tourne, on a la clé, on crée la boîte « Décision » et on lit les affaires avec leur dernière date. **Si ça ne marche pas ce soir-là, on s'arrête et on change de logiciel (ERPNext).**
- Jour 2 : les deux autres boîtes, et 30 affaires inventées.
- Jours 3-4 : le robot lit la carte, un gardien dit non, un compteur compte.
- Jours 5-6 : le chemin « affaire qui dort », avec ses portes et ses tests. Un vrai mail de test part.
- Jour 7 : la table des questions marche de bout en bout. Le non sans pourquoi est bloqué.
- Jour 8 : le robot tourne chez Amazon ou dans Docker. Le script de démo et le script qui vérifie le mode d'emploi.
- Jour 9 : vidéo, mode d'emploi, dessin, article.
- Jour 10 : on n'ajoute rien. On rejoue la démo trois fois.

Commence par me dire quelle version de Twenty, quelle version de Strands, et quelle licence Twenty a, avec les liens. Ensuite, montre-moi la liste des fichiers que tu vas créer.

# Le dessin de la maison

```
                         ┌─────────────────────────┐
                         │   Twenty (le CRM)        │
                         │  clients, affaires        │
                         └────────────┬──────────────┘
                                      │ API REST (Bearer)
                                      ▼
┌──────────────────────────────────────────────────────────────────┐
│                              LA TOUR (le robot)                    │
│                                                                      │
│  1. LA CARTE (carte.py)                                             │
│     lit Twenty une fois, garde le résultat — on ne devine jamais    │
│                                                                      │
│  2. LE CHEMIN « affaire qui dort » (relance.py + circuits.py)       │
│     classe chaque affaire : rien / relance_1 / relance_2 /          │
│     proposer_cloture / escalade                                     │
│                                                                      │
│  3. LES GARDIENS (gardefous.py)                                     │
│     liste noire · confirmation obligatoire · seuil de montant ·     │
│     quota du jour · délai minimum entre deux relances                │
│              │                              │                       │
│         AUTORISÉ                        REFUSÉ                      │
│              │                              │                       │
│              ▼                              ▼                       │
│     part tout seul               4. LA TABLE DES QUESTIONS          │
│     (Task dans Twenty)              (decisions.py)                  │
│                                      « Décision » en attente,        │
│                                      brouillon déjà écrit,           │
│                                      raison du refus                 │
│                                              │                       │
│                                              ▼                       │
│                                     LA PERSONNE dit oui / non        │
│                                     (un non sans pourquoi refusé)    │
│                                                                      │
│  5. LE CERVEAU DE SECOURS (strands_agent.py, Strands/Bedrock)        │
│     réveillé UNIQUEMENT si aucune capacité connue ne sait répondre  │
│                                                                      │
│  6. LES COMPTEURS (compteurs.py)                                    │
│     combien de fois réussi seul / combien de fois réveillé le modèle│
└──────────────────────────────────────────────────────────────────┘
```

Le chemin normal (une petite affaire qui dort, première relance) ne
touche jamais le cerveau de secours : `carte → circuits/relance →
gardefous (autorise) → Twenty`, zéro appel modèle. Le cerveau ne s'allume
que pour une capacité que rien dans `Tour.CAPACITES` ne sait faire.

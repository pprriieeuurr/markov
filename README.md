# Génération de texte avec les chaînes de Markov
Ce projet codé avec Python en 2025, majoritairement réalisé en une semaine par mes soins, permet de générer du texte grâce à une version améliorée des [Chaînes de Markov](https://fr.wikipedia.org/wiki/Cha%C3%AEne_de_Markov).
## Fonctionnement
Ce programme utilise les chaînes de Markov afin de générer une suite de mots logique.

Dans ce programme, une première étape consiste à enregistrer un graphe où les nœuds sont des mots et pour chaque mot, tous les mots qui peuvent le suivre et leur probabilité de survenir sont les arêtes. Ensuite, une seconde étape est de parcourir ce graphe pondéré en tirant au sort le mot suivant en fonction de sa probabilité d'arriver.

Le problème en faisant ainsi est que les textes n'ont aucun sens. Une ruse consiste donc à enregistrer également de quel mot on vient pour une prédiction plus précise.
## Prérequis
Pour utiliser ce projet, il faut avoir Python et installer (via pip) les bibliothèques ci-dessous :
- tqdm
- pickle
- networkx
- matplotlib
- Flask
## Installation et configuration
Pour installer et configurer le projet, il faut tout d'abord télécharger le code source de celui-ci.

Ensuite, il faut installer les dépendances dans Python 3 (celles-ci sont détaillées dans **requirements.txt** et ci-dessus).
Puis, il faut que vous exécutiez **projet.py** et que vous suiviez les étapes affichées.
## Utilisation
L'utilisation du programme peut se faire de manière intuitive via l'interface Web ou directement par ligne de code, voici les étapes à suivre
### Via l'interface Web
Exécutez le fichier app.py avec python et suivez le lien donné directement dans le terminal par Flask (pour plus d'informations, voir la [documentation officielle de Flask](https://flask.palletsprojects.com/en/stable/)).

Pour tester la génération de texte avec un des livres préinstallés, suivez les étapes une par une depuis l'interface Web.
Pour ajouter un livre au programme, ajoutez ```/add``` derrière l'URL dans la barre d'adresse (exemple ```127.0.0.1:5000/add```).
### Directement en Python
Voici un exemple de programme que vous pourriez coder afin d'utiliser ce projet sans l'interface :
```python
# Importation du module
from projet import *
# Création du graphe
extrait = GrapheMarkov("donquichotte")
# Ajout automatique d'un extrait dans le graphe.
mon_etude.ajouter_paragraphe("Bonjour, mon nom est Bob et je suis développeur web.", 3)
# Test de la prédiction
extrait.str(5, "Bob", 1)
```
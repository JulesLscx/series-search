# Series-Search Project Documentation

## Overview
Series-Search est un projet conçu pour fournir une solution de recherche et de recommandation de séries télévisées. Ce projet utilise Elasticsearch et une interface API pour gérer les requêtes et les réponses.

## Structure du Projet
Le projet est organisé en plusieurs dossiers et fichiers principaux :

- `api/`: Contient les fichiers relatifs à l'API utilisée pour les interactions avec le frontend.
- `data/`: Dossier pour stocker les données utilisées ou générées par le projet.
- `es_interface/`: Contient les scripts pour interagir avec Elasticsearch.
- `global_var.py`: Fichier pour définir les variables globales utilisées dans le projet.
- `test/`: Dossier contenant les tests pour valider les fonctionnalités du projet.
- `tools/`: Outils supplémentaires ou scripts utiles pour le projet.
- `tmp/`: Espace temporaire pour stocker des fichiers intermédiaires.
- `__main__.py`: Fichier principal pour exécuter l'application.

## Installation et Configuration

### Prérequis
- Python 3.x
- Elasticsearch

### Installation
1. Cloner le dépôt.
2. Installer les dépendances :
   ```bash
   pip install -r requirements.txt


## Utilisation

### Exécuter l'Application
Le point d'entrée principal du projet `series-search` est le fichier `__main__.py`. Pour lancer l'application, vous devez exécuter ce fichier avec Python. Selon la conception de votre application, `__main__.py` peut accepter différents arguments pour contrôler son comportement.

```bash
python __main__.py [options]

## Commande: `--example-command`

### Description
`--example-command` est une commande conçue pour [expliquez ce que fait la commande, par exemple, lancer une analyse spécifique, démarrer un serveur, etc.].

### Syntaxe
```bash
python __main__.py --example-command [options]


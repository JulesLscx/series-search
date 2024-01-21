# Installation

- [Installation](#installation)
  - [Prérequis](#prérequis)
  - [Installation](#installation-1)
    - [Configuration d'Elasticsearch](#configuration-delasticsearch)
    - [Installation des dépendances](#installation-des-dépendances)
    - [Lancement de l'application](#lancement-de-lapplication)

## Prérequis

- [Elasticsearch](https://www.elastic.co/fr/downloads/elasticsearch)
- Python 3.10 (ou supérieur)
- [pip](https://pip.pypa.io/en/stable/installation/)

## Installation

### Configuration d'Elasticsearch

Changer le mot de passe de l'utilisateur `elastic` d'Elasticsearch :

```bash
bin/elasticsearch-reset-password -u elastic -i
```
Soit mettre le mot de passe dans le fichier `global_var.py` à la ligne 4, soit le mettre dans une variable d'environnement `ES_PASSWORD`. Soit assigner le mot de passe `root_root` à l'utilisateur `elastic` d'Elasticsearch.
Vérifier aussi que le port d'Elasticsearch est bien accessible via l'url `https://localhost:9200/`. Sinon changer la variable `ES_ENDPOINT` dans le fichier `global_var.py`.
L'application créé un index `testing` assurez vous que l'index n'existe pas déjà.

### Installation des dépendances

Vous pouvez pour ne pas ruiner votre environnement python, créer un environnement virtuel, une fois dans l'envirronement virtuel, installer les dépendances avec la commande suivante :

```bash
pip install -r requirements.txt
```
ou 
```bash
pip3 install -r requirements.txt
```
Selon votre système.

### Lancement de l'application

Avant de lancer l'API ou éxécuté n'importe quelle commande il faut d'abord importer les données de `/data` dans Elasticsearch, pour cela il faut utiliser la commande suivante :

```bash
python3 __main__.py import
```
ou
```bash
python __main__.py import
```
Selon votre système.

Cette commande va importer les données dans Elasticsearch, cela peut prendre un certain temps, dépends de la puissance de votre machine.
<!-- Mettre un lien vers documentation.md -->
Une fois les données importées, vous pouvez utiliser l'application voir le fichier [documentation.md](documentation.md) pour plus d'informations.

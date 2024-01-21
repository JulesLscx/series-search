# Documentation

- [Documentation](#documentation)
  - [API](#api)
    - [Login](#login)
      - [Requête](#requête)
      - [Réponse](#réponse)
    - [Logout](#logout)
      - [Requête](#requête-1)
      - [Réponse](#réponse-1)
    - [Search](#search)
      - [Requête](#requête-2)
      - [Réponse](#réponse-2)
    - [Create User](#create-user)
      - [Requête](#requête-3)
      - [Réponse](#réponse-3)
    - [Delete User](#delete-user)
      - [Requête](#requête-4)
      - [Réponse](#réponse-4)
    - [Edit User](#edit-user)
      - [Requête](#requête-5)
      - [Réponse](#réponse-5)
    - [Series](#series)
      - [Requête](#requête-6)
      - [Réponse](#réponse-6)
    - [Find serie by id](#find-serie-by-id)
      - [Requête](#requête-7)
    - [Réponse](#réponse-7)
    - [Watched](#watched)
      - [Requête](#requête-8)
      - [Réponse](#réponse-8)
    - [Add new watched serie](#add-new-watched-serie)
      - [Requête](#requête-9)
      - [Réponse](#réponse-9)
    - [Recommendate](#recommendate)
      - [Requête](#requête-10)
      - [Réponse](#réponse-10)
  - [CLI](#cli)
    - [Liste des commandes](#liste-des-commandes)
    - [Recherche](#recherche)
    - [Recommandation](#recommandation)

<!-- Saute une page -->
<div style="page-break-after: always;"></div>

## API

    Quand l'API est lancée elle est par défaut sur le port 5000, vous pouvez y accéder via l'URL : http://localhost:5000/serie-search/
Pour tester l'API vous essayer d'accéder à l'URL http://localhost:5000/serie-search/ et une page web devrait s'afficher. Si ce n'est pas le cas, vérifier que vous avez bien installé les dépendances et que vous avez bien lancé l'API.

### Login

#### Requête

`POST /login`

```json
{
  "name" : "your_account",
  "password" : "your_password"
}
```
Par défaut il y a deux comptes : admin et user, le mot de passe est le même pour les deux : your_password

#### Réponse

```json
{
  "message": "Login failed|succesful"
}
```
Et un cookie de session est créé si le login est réussi.

### Logout

#### Requête

Cette opération nécessite d'être authentifié.
`GET /logout`

#### Réponse

```json
{
  "message": "Logout successful"
}
```
Si le logout est réussi le cookie de session est supprimé.

### Search

#### Requête

Cette opération nécessite ne nécessite pas d'authentification.
`GET /search/<query>`

- query correspond à la requête de recherche.
#### Réponse

```json
{
  "1": "theoc",
  "2": "weeds",
  "3": "alias",
  "4": "coldcase",
  "5": "criminalminds",
  "6": "daybreak",
  "7": "ghostwhisperer",
  "8": "leverage",
  "9": "ncis",
  "10": "painkillerjane"
}
```
La réponse contient les résultats de la recherche sous forme de dictionnaire. La clé est le classement de la pertinence de la recherche et la valeur est le nom de la série.

### Create User

#### Requête

Cette opération nécessite d'être authentifié et d'avoir le rôle d'admin.

`POST /admin/user/create`

```json
{
  "name":"your_account",
  "password":"your_password",
  "role":0
}
```
Le rôle 0 correspond à un utilisateur normal et le rôle 1 correspond à un administrateur.

#### Réponse

```json
{
  "message": "User created"
}
```

### Delete User

#### Requête

Cette opération nécessite d'être authentifié et d'avoir le rôle d'admin.

`DELETE /admin/user/delete/<user>`

- user correspond au nom de l'utilisateur que vous voulez supprimer.
#### Réponse

```json
{
  "message": "User deleted"
}
```

### Edit User

#### Requête

Cette opération nécessite d'être authentifié et d'avoir le rôle d'admin.
Vous pouvez modifier le rôle d'un utilisateur et/ou son mot de passe.

`PUT /admin/user/edit/<user>`

- user correspond au nom de l'utilisateur que vous voulez modifier.
```json
{
  "role":1
}
```

#### Réponse

```json
{
  "message": "User edited"
}
```
### Series

#### Requête

Cette opération ne nécessite pas d'authentification.

`GET /series/`

#### Réponse

```json
{
    [
        { 
            "id":1,
            "title":"The O.C."
        },
        { 
            "id":2,
            "title":"Weeds"
        },
        ...
        {
             "id":120,
            "title":"Painkiller Jane"
        }
    ]
}
```

### Find serie by id

#### Requête

Cette opération ne nécessite pas d'authentification.

`GET /series/<id>`

- id correspond à l'id de la série que vous voulez trouver.
### Réponse

```json
{
    "id":1,
    "title":"The O.C."
}
```
ou 
```json
{
    "message": "Serie not found"
}
```

### Watched

#### Requête

Cette opération nécessite d'être authentifié.

`GET /watched/`

#### Réponse

```json
{
  [ "theoc", "weeds", "alias", "coldcase", "criminalminds", "daybreak", "ghostwhisperer", "leverage", "ncis", "painkillerjane" ]
}
```
ou 
```json
{
  "message": "No watched series"
}
```

### Add new watched serie

#### Requête

Cette opération nécessite d'être authentifié.

`POST /watched/<id>`

- id correspond à l'id de la série que vous voulez ajouter.

#### Réponse

```json
{
  "message": "Serie added"
}
```

### Recommendate

#### Requête

Cette opération nécessite d'être authentifié. Et il faut avoir au moins une série dans la liste des séries regardées.

`GET /recommendate/`

#### Réponse

```json
{
  "1": "theoc",
  "2": "weeds",
  "3": "alias",
  "4": "coldcase",
  "5": "criminalminds",
  "6": "daybreak",
  "7": "ghostwhisperer",
  "8": "leverage",
  "9": "ncis",
  "10": "painkillerjane"
}
```

## CLI

Vous pouvez aussi ne pas lancer l'API et pour tester la recherche et la recommandation vous pouvez utiliser le CLI.

### Liste des commandes

- `unzip <path>` : Dézippe les fichiers de séries dans le dossier spécifié par `<path>`. et les met dans le dossier `data`.
- `import` : Importe les documents du dossier `data` dans ElasticSearch.
- `query <text>` : Recherche les séries correspondant au texte `<text>`.
- `score_search` : Lance les tests de recherche.
- `recommand` : Lance les tests de recommandation.
- `test_api` : Lance les tests de l'API.
- `run_api` : Lance l'API.
- `help` : Affiche l'aide.


### Recherche

`python3 __main__.py query <text>`
Exemple : `python3 __main__.py query "comté orange"`

### Recommandation

`python3 __main__.py recommand`

Lance la recommendation pour quelqu'un qui a vu les séries suivantes: 
```python
["alias", "ncis", "24", "breakingbad", "prisonbreak",'smallville', 'stargatesg1', 'friends', 'scrubs', 'charmed', 'southpark', 'bones', 'xfiles', 'onetreehill', 'lost','criminalminds', 'entourage', 'buffy', 'coldcase', 'supernatural', 'desperatehousewives', 'greysanatomy', 'doctorwho', 'intreatment', 'theoc','howimetyourmother', 'uglybetty', 'angel', 'ghostwhisperer', 'medium', 'thesopranos', 'niptuck', 'thepretender', 'veronicamars', 'weeds']
```

# Connaissances et Raisonnement | Système de Recommandation de Films

L'application est disponible aux adresses suivantes : [cr.pesch.fr](https://cr.pesch.fr/) et [cr.pebernard.tk](https://cr.pebernard.tk).

## Description du projet

### Concept de l'application

L'application permet de sélectionner des films et de se voir proposer au fur et à mesure des films pertinents en fonction de ceux déjà choisis.

Dès l'arrivée sur l'application, 12 films sont affichés. 

Pour chacun d'entre eux il est possible de consulter entre autres :
- Un court résumé du film
- La durée du film
- L'année de sortie du film
- Les genres associés à ce film
- Le(s) réalisateur(s) du film
- Le casting du film

Il est ensuite possible de choisir un film en cliquant sur la flèche : 12 nouveaux films dérivés de ce choix seront ensuite proposés.

Le processus peut ensuite être répété jusqu'à trouver un film qui plaît à l'utilisateur.

### Base de connaissances sur les films

Nous avons utilisé l'API de [The Movie Database (_TMDb_)](https://www.themoviedb.org/) accessible [ici](https://www.themoviedb.org/documentation/api).
_TMDb_ est une base de données communautaire de films et de séries TV. 
Les données relatives aux films et séries TV ont été ajoutées par l'ensemble des membres de la communauté.

### Principe de recommandation

L'application utilise les acteurs et le réalisateur des derniers choix ainsi que les genres pour trouver de nouvelles propositions.

## Descriptif technique

Le code de l'application est disponible sur [GitHub](https://github.com/mathispesch/cr-recommendations).

Au niveau technique, nous avons programmé en _Python_ (avec _Flask_ notamment) et utilisé le framework Javascript
[_Vue.js_](https://vuejs.org/) afin de développer l'interface web.

### Arborescence du projet

```
.
├── static      Interface en Vue.js
├── app.py      Application Web développée en Flask
└── tmdb.py     Module pour faire des requêtes TMDB
```

### Lancer le projet en local

1. Installer les dépendances :
    ```
    pip install -r requirements.txt
    ```

2. Paramétrer les variables d'environnement :
   1. Copier le fichier `.env.template` dans un fichier `.env`.
   2. Remplir les variables `SECRET` et `TMDB_TOKEN` (clé d'API).


3. Lancer l'application Flask en tapant dans un terminal :
   
   - en mode développement
   ```
   FLASK_APP=app.py flask run
   ```
   - ou en mode production
    ```
    gunicorn --bind 0.0.0.0:5000 wsgi:app
    ```

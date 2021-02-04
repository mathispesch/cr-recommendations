# Connaissances et Raisonnement | Système de Recommandation de Films

## Description du projet

### Concept de l'application

Dès l'arrivée sur l'application, 12 films sont affichés. 
Pour chacun d'entre eux vous pouvez consulter entre autres :
- Un court résumé du film
- Les genres associés à ce film
- La durée du film
- Le(s) réalisateur(s) du film
- Le casting du film

Vous pouvez ensuite choisir un film en cliquant sur la flèche. 
12 nouveaux films dérivés de votre choix vous seront ainsi proposés. 
Vous pouvez ensuite répéter le processus jusqu'à trouver un film qui vous plaît.

### Base de connaissances sur les films

Nous avons utilisé l'API de [The Movie Database (_TMDb_)](https://www.themoviedb.org/) accessible [ici](https://www.themoviedb.org/documentation/api).
_TMDb_ est une base de données communautaire de films et de séries TV. 
Les données relatives aux films et séries TV ont été ajoutées par l'ensemble des membres de la communauté.


### Principe de recommandation



## Descriptif technique

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

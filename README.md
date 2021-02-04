# Connaissances et Raisonnement | Système de Recommandation de Films

## Description du projet

## Descriptif technique

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

# CR-Recommendations

```
.
├── static      Vue front-end
├── app.py      Flask app
└── tmdb.py     TMDB wrapper
```

## How to run

1. Install the requirements:
    ```
    pip install -r requirements.txt
    ```

2. Set-up the environment variables:
   1. Copy the `.env.template` file to a new `.env` file.
   2. Populate the `SECRET` and `TMDB_TOKEN` (bearer token) variables.

3. Run the Flask app with:
    ```
    gunicorn --bind <ADDRESS>:<PORT> wsgi:app
    ```
    
    example:
    `gunicorn --bind 0.0.0.0:5000 wsgi:app`
    will listen on all interfaces on port `5000`

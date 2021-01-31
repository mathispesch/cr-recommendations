import os
import random

import requests

BEARER_TOKEN = os.getenv("TMDB_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {BEARER_TOKEN}"
}
PARAMS = {
    "language": "fr-FR",
    "region": "FR"
}

BASE_API = "https://api.themoviedb.org/3/"


def get_movies(n, filters=dict):
    movies = []
    for i in range(3 * n // 20 + 1):
        r = requests.get(f"{BASE_API}/discover/movie", headers=HEADERS, params={**PARAMS, "page": i + 1})
        if not r.ok:
            print(r.json())
            raise Exception("TMDB Error")

        movies += r.json()["results"]

    movies = random.choices(movies, k=10)
    random.shuffle(movies)

    return movies


def get_movie(_id):
    r = requests.get(
        f"{BASE_API}/movie/{_id}", headers=HEADERS, params={**PARAMS, "append_to_response": "keywords, credits"}
    )
    if not r.ok:
        raise Exception("TMDB Error")

    return r.json()

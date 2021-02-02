import os
import random

import requests
from flask.cli import load_dotenv

assert load_dotenv(), "Unable to load .env"

BEARER_TOKEN = os.getenv("TMDB_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {BEARER_TOKEN}"
}
PARAMS = {
    "language": "fr-FR",
    "region": "FR"
}

BASE_API = "https://api.themoviedb.org/3/"


def get_movies(n):
    s = requests.session()
    movies = []
    for i in range(3 * n // 20 + 1):
        r = s.get(f"{BASE_API}/discover/movie", headers=HEADERS, params={**PARAMS, "page": i + 1})
        if not r.ok:
            print(r.json())
            raise Exception("TMDB Error")

        movies += r.json()["results"]

    movies = random.sample(movies, n)

    return movies


def get_movie(_id):
    r = requests.get(
        f"{BASE_API}/movie/{_id}", headers=HEADERS, params={**PARAMS, "append_to_response": "keywords,credits"}
    )
    if not r.ok:
        raise Exception("TMDB Error")

    return r.json()


def get_movies_filtered(with_crew=None, with_cast=None, with_people=None, with_keywords=None, with_genres=None):
    s = requests.session()
    filters = {}

    if with_crew:
        filters["with_crew"] = "|".join([str(el) for el in with_crew])
    if with_cast:
        filters["with_cast"] = "|".join([str(el) for el in with_cast])
    if with_people:
        filters["with_people"] = "|".join([str(el) for el in with_people])
    if with_keywords:
        filters["with_keywords"] = "|".join([str(el) for el in with_keywords])
    if with_genres:
        filters["with_genres"] = "|".join([str(el) for el in with_genres])

    r = s.get(f"{BASE_API}/discover/movie", headers=HEADERS, params={**PARAMS, **filters})
    if not r.ok:
        print(r.json())
        raise Exception("TMDB Error")

    return r.json()["results"]


def get_recommendations(n, params):
    movies = []

    if params.get("genres", []):
        results = get_movies_filtered(with_genres=params["genres"])
        movies += results

    if params.get("keywords", []):
        results = get_movies_filtered(with_keywords=params["keywords"])
        movies += results

    if params.get("cast", []):
        results = get_movies_filtered(with_cast=params["cast"])
        movies += results

    if params.get("crew", []):
        results = get_movies_filtered(with_crew=params["crew"])
        movies += results

    movies = list(filter(lambda m: m["id"] not in params.get("seen", []), movies))

    if len(movies) < n:
        # Add movies if there is not enough
        movies += get_movies(n)
        # Filter to remove movies already seen
        movies = list(filter(lambda m: m["id"] not in params.get("seen", []), movies))

    # TODO Remove duplicates
    movies = random.sample(movies, n)
    return movies

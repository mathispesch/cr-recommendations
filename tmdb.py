import datetime
import os
import random

import numpy
import requests
from flask.cli import load_dotenv

assert load_dotenv(), "Unable to load .env"

BEARER_TOKEN = os.getenv("TMDB_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {BEARER_TOKEN}"
}
PARAMS = {
    "language": "fr-FR",
    "region": "FR",
}
DISCOVER_PARAMS = {
    "with_runtime.gte": 15,
    "release_date.lte": datetime.date.today().isoformat(),
}

BASE_API = "https://api.themoviedb.org/3/"


def get_movies(n):
    """Get n popular movies."""
    s = requests.session()
    movies = []
    for i in range(6 * n // 20 + 1):
        r = s.get(f"{BASE_API}/discover/movie", headers=HEADERS, params={**PARAMS, **DISCOVER_PARAMS, "page": i + 1})
        if not r.ok:
            print(r.json())
            raise Exception("TMDB Error")

        movies += r.json()["results"]

    movies = random.sample(movies, min(len(movies), n))

    return movies


def get_movie(_id):
    """Get the details of a specific movie."""
    r = requests.get(
        f"{BASE_API}/movie/{_id}", headers=HEADERS, params={**PARAMS, "append_to_response": "credits"}
    )
    if not r.ok:
        raise Exception("TMDB Error")

    return r.json()


def get_movies_filtered(with_people=None, with_genres=None, page=1):
    """Get movies with filters based on people (cast and crew) and genres."""
    s = requests.session()
    filters = {"page": page}

    if with_people:
        filters["with_people"] = "|".join([str(el) for el in with_people])
    if with_genres:
        filters["with_genres"] = "|".join([str(el) for el in with_genres])

    r = s.get(f"{BASE_API}/discover/movie", headers=HEADERS, params={**PARAMS, **DISCOVER_PARAMS, **filters})
    if not r.ok:
        print(r.json())
        raise Exception("TMDB Error")

    result = r.json()
    return result["results"], result["total_pages"]


def get_recommendations(n, params):
    """Get n movie recommendations.

    This retrieves movies based on some filters (cast, crew and genres) and adds other movies and some
    movies that have already been presented to the user.
    """
    movies = []
    seen_movies = []

    seen = params.get("seen", [])

    if params.get("genres"):
        current_page = 1
        max_page = 2
        new_results = 0
        while current_page <= max_page and new_results < 12:
            page_results, max_page = get_movies_filtered(with_genres=params["genres"], page=current_page)
            current_page += 1
            new_results += len([1 for r in page_results if r["id"] not in seen])
            movies += page_results

    if params.get("cast") or params.get("crew"):
        people = params.get("cast", []) + params.get("crew", [])
        current_page = 1
        max_page = 2
        new_results = 0
        while current_page <= max_page and new_results < 12:
            page_results, max_page = get_movies_filtered(with_people=people)
            current_page += 1
            new_results += len([1 for r in page_results if r["id"] not in seen])
            movies += page_results

    if len([1 for m in movies if m["id"] not in seen]) < n:
        current_page = 1
        max_page = 2
        results = []
        while current_page <= max_page and len(results) < 12:
            results, max_page = get_movies_filtered()
            results = list(filter(lambda m: m["id"] not in seen, results))
            current_page += 1
            movies += results

    # Remove duplicates and movies that have already been chosen
    filtered_movies = []
    for movie in movies + seen_movies:
        if movie["id"] not in [m["id"] for m in filtered_movies] and movie["id"] not in params["choices"]:
            filtered_movies.append(movie)

    p = [1 if m["id"] in seen else 10 for m in filtered_movies]
    filtered_movies = numpy.random.choice(
        filtered_movies,
        size=min(len(filtered_movies), n),
        replace=False,
        p=[el / sum(p) for el in p]
    ).tolist()

    return filtered_movies

import os

from flask import Flask, jsonify, request, session
from flask.cli import load_dotenv
from flask_cors import CORS
from flask_caching import Cache

import tmdb

assert load_dotenv(), "Unable to load .env"

app = Flask(__name__, static_url_path='')
app.secret_key = os.getenv("SECRET")
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
CORS(app, resources={r"/*": {"origins": "*"}})


@cache.memoize()
def _get_movie(_id):
    return tmdb.get_movie(_id)


@app.route("/")
def get_app():
    return app.send_static_file("index.html")


@app.route("/api/movies")
def get_n():
    n = request.args.get("n", 12)
    if not (5 < n < 20):
        return jsonify({"success": False, "error": "n must be between 5 and 20."}), 400

    if "choices" not in session:
        # The user has not choosen a movie yet
        movies = tmdb.get_movies(n)
    else:
        # The user has already choosen at least one movie
        params = {
            "seen": session["seen"],
            "genres": session["genres"],
            "keywords": session["keywords"],
            "cast": session["cast"],
            "crew": session["crew"],
        }
        movies = tmdb.get_recommendations(n, params)  # TODO: search and choose relevant movies

    session["current_ids"] = [m["id"] for m in movies]

    return jsonify({"success": True, "movies": movies})


@app.route("/api/choice", methods=["POST"])
def post_choice():
    if not request.json or "choice" not in request.json:
        return jsonify({"success": False, "error": "You must submit a movie choice."}), 400

    chosen_id = request.json["choice"]
    movie = _get_movie(chosen_id)
    genres = [el["id"] for el in movie["genres"]]
    keywords = [el["id"] for el in movie["keywords"]["keywords"]]
    cast = [el["id"] for el in movie["credits"]["cast"] if el["order"] <= 3]
    crew = [el["id"] for el in movie["credits"]["crew"] if
            (el["job"], el["department"]) == ("Director", "Directing")]

    session["choices"] = session.get("choices", []) + [chosen_id]
    session["seen"] = list(set(session.get("seen", []) + session.get("current_ids", [])))
    session["genres"] = list(set(session.get("genres", []) + genres))
    session["keywords"] = list(set(session.get("keywords", []) + keywords))
    session["cast"] = list(set(session.get("cast", []) + cast))
    session["crew"] = list(set(session.get("crew", []) + crew))

    return jsonify({"success": True})


@app.route("/api/details/<_id>")
def get_details(_id):
    return jsonify({"success": True, "details": _get_movie(_id)})


@app.route("/api/reset", methods=["POST"])
def reset():
    if "choices" in session:
        session.pop("choices")
    if "seen" in session:
        session.pop("seen")
    if "current_ids" in session:
        session.pop("current_ids")
    if "genres" in session:
        session.pop("genres")
    if "cast" in session:
        session.pop("cast")
    if "keywords" in session:
        session.pop("keywords")
    if "crew" in session:
        session.pop("crew")

    return jsonify({"success": True})

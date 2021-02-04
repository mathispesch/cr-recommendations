import os

from flask import Flask, jsonify, request, session
from flask.cli import load_dotenv
from flask_caching import Cache
from flask_cors import CORS

import tmdb

assert load_dotenv(), "Unable to load .env"

app = Flask(__name__, static_url_path='')
app.secret_key = os.getenv("SECRET")
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
CORS(app, resources={r"/*": {"origins": "*"}})


@cache.memoize()
def _get_movie(_id):
    """This is a cached helper function returning the details of a movie."""
    return tmdb.get_movie(_id)


@app.route("/")
def get_app():
    """Serve the Vue.js app."""
    return app.send_static_file("index.html")


@app.route("/api/movies")
def get_n():
    """Return n movies.

    Depending on the state of the app (cookies), this returns movies either randomly selected among
    popular movies or selected among movies that have similar characteristics to the one already chosen
    by the user.
    """
    n = request.args.get("n", 12)
    if not (5 < n < 20):
        return jsonify({"success": False, "error": "n must be between 5 and 20."}), 400

    if "choices" not in session:
        # The user has not chosen a movie yet
        movies = tmdb.get_movies(n)
    else:
        # The user has already chosen at least one movie
        params = {
            "seen": session["seen"],
            "genres": session["genres"],
            "cast": session["cast"],
            "crew": session["crew"],
            "choices": session["choices"]
        }
        movies = tmdb.get_recommendations(n, params)

    # Store the sent ids, this is used to store the movies seen by the user when they choose a movie
    session["current_ids"] = [m["id"] for m in movies]

    return jsonify({"success": True, "movies": movies})


@app.route("/api/choice", methods=["POST"])
def post_choice():
    """Post the choice of a movie by the user."""
    if not request.json or "choice" not in request.json:
        return jsonify({"success": False, "error": "You must submit a movie choice."}), 400

    # Retrieve the details of the movie
    chosen_id = request.json["choice"]
    movie = _get_movie(chosen_id)

    # Retrieve the characteristics of the movie and add it to the session
    genres = [el["id"] for el in movie["genres"]]
    cast = [el["id"] for el in movie["credits"]["cast"] if el["order"] <= 3]
    crew = [el["id"] for el in movie["credits"]["crew"] if
            (el["job"], el["department"]) == ("Director", "Directing")]

    session["choices"] = session.get("choices", []) + [chosen_id]
    session["seen"] = list(set(session.get("seen", []) + session.get("current_ids", [])))
    session["genres"] = list(set(session.get("genres", []) + genres))
    session["crew"] = list(set(session.get("crew", []) + crew))

    # Do not use the cast of animated movies
    if "Animation" not in [g["name"] for g in movie["genres"]]:
        session["cast"] = list(set(session.get("cast", []) + cast))
    else:
        session["cast"] = session.get("cast", [])

    return jsonify({"success": True})


@app.route("/api/details/<_id>")
def get_details(_id):
    """Returns the details of a movie."""
    return jsonify({"success": True, "details": _get_movie(_id)})


@app.route("/api/reset", methods=["POST"])
def reset():
    """Resets the session for an user."""
    for k in list(session.keys()):
        session.pop(k)

    return jsonify({"success": True})

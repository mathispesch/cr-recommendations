import os

from flask import Flask, jsonify, request, session
from flask_cors import CORS

import tmdb

app = Flask(__name__)
app.secret_key = os.getenv("SECRET")
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/movies")
def get_n():
    n = request.args.get("n", 12)
    if not (5 < n < 20):
        return jsonify({"success": False, "error": "n must be between 5 and 20."}), 400

    if "choices" not in session:
        # The user has not choosen a movie yet
        movies = tmdb.get_movies(n)
    else:
        # The user has already choosen at least one movie
        movies = tmdb.get_movies(n)  # TODO: search and choose relevant movies

    return jsonify({"success": True, "movies": movies})


@app.route("/choice", methods=["POST"])
def post_choice():
    if not request.json or "choice" not in request.json:
        return jsonify({"success": False, "error": "You must submit a movie choice."}), 400

    if "choices" not in session:
        session["choices"] = []

    session["choices"] = session["choices"] + [request.json["choice"]]

    return jsonify({"success": True})


@app.route("/details/<_id>")
def get_details(_id):
    return jsonify({"success": True, "details": tmdb.get_movie(_id)})


@app.route("/reset", methods=["POST"])
def reset():
    if "choices" in session:
        session.pop("choices")

    return jsonify({"success": True})

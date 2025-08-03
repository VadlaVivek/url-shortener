# app/main.py
from flask import Flask, request, jsonify, redirect, abort
from app.models import URLStore
from app.utils import generate_short_code, is_valid_url

app = Flask(__name__)
store = URLStore()

@app.route("/")
def health_check():
    return jsonify({"status": "ok"})

@app.route("/api/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "Missing URL"}), 400

    original_url = data["url"]
    if not is_valid_url(original_url):
        return jsonify({"error": "Invalid URL"}), 400

    short_code = generate_short_code()
    while store.get(short_code):
        short_code = generate_short_code()

    store.add(short_code, original_url)
    return jsonify({
        "short_code": short_code,
        "short_url": f"http://localhost:5000/{short_code}"
    }), 201

@app.route("/<short_code>", methods=["GET"])
def redirect_to_url(short_code):
    record = store.get(short_code)
    if not record:
        abort(404)

    store.increment_clicks(short_code)
    return redirect(record["url"])

@app.route("/api/stats/<short_code>", methods=["GET"])
def get_stats(short_code):
    record = store.get(short_code)
    if not record:
        abort(404)

    return jsonify({
        "url": record["url"],
        "clicks": record["clicks"],
        "created_at": record["created_at"].isoformat() + "Z"
    })

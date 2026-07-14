from flask import Flask, render_template, request, send_from_directory
from pathlib import Path

from src.database import Database

app = Flask(__name__)

VIDEO_FOLDER = Path("videos/input")


@app.route("/")
def index():
    query = request.args.get("q", "").strip()

    db = Database()

    results = []

    if query:
        results = db.search(query)

    db.close()

    return render_template(
        "index.html",
        query=query,
        results=results
    )


@app.route("/videos/<path:filename>")
def video(filename):
    return send_from_directory(VIDEO_FOLDER, filename)


if __name__ == "__main__":
    app.run(debug=True)
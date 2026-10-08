from flask import Flask, abort, render_template
from datetime import datetime
from dotenv import find_dotenv, load_dotenv

from azure_web_app import auth, db
from azure_web_app._constants import SECRET_ENV_FILE

FAVORITES = [
    {"id": 1, "title": "Mike Hundt ", "why": "Rapier vibing"},
    {"id": 2, "title": "Liechtenaur", "why": "the og"},
    {"id": 3, "title": "Sellsword Arts", "why": "Modern entertainment"},
]

def create_app():
    load_dotenv(find_dotenv(SECRET_ENV_FILE))
    app = Flask(__name__)
    db.setup_for_app(app)
    auth.setup_auth(app)
    setup_routes(app)
    return app


def index():
    return render_template(
        "index.html",
        name="<em>YOUR NAME</em>",
        hobby="sword fighting",
        hours_per_week=14,  # roughly how many hours a week you spend on it
        fun_fact="violence",
        favorite=FAVORITES,
        hour=datetime.now().hour,
        show_counter=False,
    )

def setup_routes(app):
    app.route("/")(index)


def run_app(debug: bool = True) -> None:
    app = create_app()
    app.run(debug=debug)

def favorite_detail(favorite_id: int):
    for favorite in FAVORITES:
        if favorite["id"] == favorite_id:
            return render_template("favorite.html", favorite=favorite)
    abort(404)


def setup_routes(app):
    app.route("/")(index)
    app.route("/favorites/<int:favorite_id>")(favorite_detail)

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

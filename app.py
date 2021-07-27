from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("database")
db = SQLAlchemy(app)

result = db.session.execute("SELECT * FROM words").fetchall()
print(result)

@app.route("/")
def index(): 
    return render_template("intro.html")

@app.route("/new_user")
def new_user():
    return "new user registration page"

@app.route("/play_game")
def play_game():
    return render_template("play_game.html")

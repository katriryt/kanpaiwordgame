from flask import Flask
from flask import render_template

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/")
def index(): 
    return render_template("intro.html")

@app.route("/new_user")
def new_user():
    return "new user registration page"

@app.route("/play_game")
def play_game():
    return "game page"

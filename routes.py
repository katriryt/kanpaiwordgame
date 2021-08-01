from app import app
from flask import render_template, request, redirect, session, make_response
import game_contents, users

@app.route("/")
def index(): 
    return render_template("intro.html")

@app.route("/play_game")
def play_game():

    if 'rndnm' in request.args:
#        print('test')
        if request.args['rndnm'] == '-1':
#            print('starting new game')
#            print(session)
            temp = session['gameinfo']
            newround = int(request.args['rndnm']) + 1
            temp['roundnumber'] = newround
#            print(temp)
            session['gameinfo'] = temp
        else:
#            print('playing game')
            temp = session['gameinfo']
            newround = int(temp['roundnumber']) + 1
            temp['roundnumber'] = newround
            session['gameinfo'] = temp
    else:
#        print('no arguments sent')
        pass

    game_names=game_contents.get_game_names()
    series_cards=game_contents.one_series_game_cards()
#    print("")
#    print(series_cards)

    return render_template("play_game.html",
    game_names=game_names, 
    series_cards=series_cards
    )

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method=="GET":
        return render_template("signup.html")

    if request.method=="POST":
        username = request.form["username"] 
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        role = request.form["role"]

        if username == "":
            return render_template("error.html", message="Please insert a username")

        if len(username) < 2 or len(username) > 5:
            return render_template("error.html", message="User name must be 2-5 characters long, please try again")

        if users.check_user_name_exists(username) is False:
            return render_template("error.html", message="Please choose another username")

        if password1 == "" or password2 == "":
            return render_template("error.html", message="Please insert a password")

        if len(password1) < 2 or len(password1) > 5:
            return render_template("error.html", message="Password must be 2-5 characters long, please try again")

        if len(password2) < 2 or len(password2) > 5:
            return render_template("error.html", message="Password must be 2-5 characters long, please try again")

        if password1 != password2:
            return render_template("error.html", message="Passwords did not match, please try again")

        if role != "1" and role != "2":
            return render_template("error.html", message="Please select a role from the drop down menu")

        if users.signup(username, password1, role):
            return redirect("/play_game")

        else:
            return render_template("error.html", message="Registration was not successful, please try again")

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method=="GET":
        return render_template("signin.html")

    if request.method=="POST":
        print("writing something")
        username = request.form["username"] 
        password = request.form["password"]

        if username == "":
            return render_template("error.html", message="Please insert a username")

        if len(username) < 2 or len(username) > 5:
            return render_template("error.html", message="User name must be 2-5 characters long, please try again")

        if users.check_user_name_exists(username) is True:
            return render_template("error.html", message="No such user name exists, please register")        

        if password == "":
            return render_template("error.html", message="Please insert a password")

        if len(password) < 2 or len(password) > 5:
            return render_template("error.html", message="Password must be 2-5 characters long, please try again")

        if users.signin(username, password):
            print("sign-in ok")
            return redirect("/play_game")

        else:
            return render_template("error.html", message="Password was not correct, please try again") 

@app.route("/signout")
def signout():
    users.signout()
    return redirect("/")

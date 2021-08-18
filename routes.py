from app import app
from flask import render_template, request, redirect, session, make_response
import game_contents, users, game

@app.route("/")
def index(): 
    return render_template("intro.html")

@app.route("/play_game")
def play_game():

    if 'rndnm' in request.args: # pitänee varmistaa, että muuttujat nollia
#        print('test')
        if request.args['rndnm'] == '-1':
            print('starting new game')
#            print(session)
            temp = session['gameinfo']
#            print(temp)
            newround = int(request.args['rndnm']) + 1
            temp['roundnumber'] = newround
#            print(temp)
            session['gameinfo'] = temp
#            print(temp)
#            print(session)
        else:
            print('playing game')
            pass
#            print(session)
#            temp = session['gameinfo']
#            newround = int(temp['roundnumber']) + 1
#            temp['roundnumber'] = newround
#            temp['gamename'] = 'Greetings' # Näin voidaan muuttaa pelin nimeä
#            session['gameinfo'] = temp
#            print(session)
#            print(temp)
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

@app.route("/processinput", methods=["post"])
def processinput():
    result = request.json['wasright']
#    print(result)
#    print("")
#    print(session)
#    print(request)
#    print(request.json)
#    print(request.json['wasright'])

#    print(session['gameinfo']['roundnumber'])
    session['gameinfo']['roundnumber'] +=1
#    print(session['gameinfo']['roundnumber'])

#    print(session['gameinfo']['correctanswers'])

    if result == 1: 
#        print("was correct")
#        print(session['gameinfo']['correctanswers'])
        session['gameinfo']['correctanswers'] += 1
#        print(session['gameinfo']['correctanswers'])

    print(session)
    print(session['gameinfo']['maxrounds'])    

    session.modified = True

    if session['gameinfo']['roundnumber'] >= session['gameinfo']['maxrounds']-1:
        print("rounds are done, time to save the results")
        game.save_game_results(session['gameinfo']['gamename'], session['user_id'], session['csrf_token'], session['gameinfo']['words_total'], session['gameinfo']['correctanswers'])
#        game.save_game_results(game_class, player_id, session_id, total_words, words_correct)

#    print(session)

    return ('', 200)


@app.route("/signup", methods=["get", "post"])
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

@app.route("/signin", methods=["get", "post"])
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

@app.route("/feedback", methods=["get", "post"])
def feedback():
    print("feedback:ssa")
    if request.method =="GET": 
        print("muoto on get")
        return render_template("feedback.html")

    if request.method =="POST":
        print("metodi on post")
        users.check_csrf()
        
        game_class = request.form["gamename"]
        player_id = request.form["player_id"]
        session_id = request.form["session_id"]
        points = int(request.form["stars"])
        if points < 1 or points > 5: 
            return render_template("error.html", message="Please select a number between 1 and 5")
        comments = request.form["comments"]
        if len(comments) > 2000: 
            return render_template("error.html", message="Please write a shorter comment")
        if comments =="":
            comments ="N/A"
        
        print(game_class, player_id, session_id, points, comments)
        game.save_feedback(game_class, player_id, session_id, points, comments)

        #return redirect("/feedback")
        return ('', 204)
        

@app.route("/signout")
def signout():
    users.signout()
    return redirect("/")

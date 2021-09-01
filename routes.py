from app import app
from flask import render_template, request, redirect, session, make_response
import game_contents, users, game, data_statistics

@app.route("/")
def index(): 
    return render_template("intro.html")

@app.route("/play_game")
def play_game():
    users.require_role(1)

    if 'restart' in request.args:
        restart_message = request.args['restart']
        if restart_message == 'yes':
#            print(session['gameinfo']['gamename'])
            wanted_game = session['gameinfo']['gamename']
#            print('asking for restart for : ' + wanted_game)
            game.restart_game(wanted_game)

    if 'changegame' in request.args:
#        print(session['gameinfo']['gamename'])
        change_game_message = request.args['changegame']
#        print('asking for new game with: ' + change_game_message)
        all_game_names = game_contents.get_game_names()
#        print(all_game_names)
        if change_game_message in all_game_names:
            game.restart_game(change_game_message)
        else:
            return render_template("error.html", message="Game does not exist")

    if session['gameinfo']['roundnumber']+1 > session['gameinfo']['maxrounds']:
#        print('print, oli jo maksimissa, jatketaan samalla pelillä')
        continue_current_game = session['gameinfo']['gamename']
        game.restart_game(continue_current_game)

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
#    print("process input tsekkauksessa")
    users.require_role(1)
    users.check_ajax_csrf(request.json['session_id'])
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

#    print(session)
#    print(session['gameinfo']['maxrounds'])    

    session.modified = True
#    print(session)

    if session['gameinfo']['roundnumber'] >= session['gameinfo']['maxrounds']-1:
#        print("rounds are done, time to save the results")
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
#        print("writing something")
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
#    print("feedback:ssa")
    users.require_role(1)
    if request.method =="GET": 
#        print("muoto on get")
        return render_template("feedback.html")

    if request.method =="POST":
#        print("metodi on post")
        users.check_form_csrf()
        
        game_class = request.form["gamename"]
        player_id = request.form["player_id"]
        session_id = request.form["session_id"]
        points = int(request.form["stars"])
        if points < 1 or points > 5: 
            return render_template("error.html", message="Please select a rating between 1 and 5")
        comments = request.form["comments"]
        if len(comments) > 200: 
            return render_template("error.html", message="Please write a shorter comment")
        if comments =="":
            comments ="N/A"
        
#        print(game_class, player_id, session_id, points, comments)
        game.save_feedback(game_class, player_id, session_id, points, comments)

        #return redirect("/feedback")
        return ('', 204)
        
@app.route("/statistics")
def statistics():
#    print("tilasto-sivulla")
    users.require_role(1)
#    game_names = game_contents.get_game_names()
    player_id = session['user_id']
    user_stats = data_statistics.user_statistics(player_id)
#    print(user_stats)
#    return render_template("statistics.html", game_names=game_names, user_stats=user_stats)
    best_game_stats = data_statistics.best_game_statistics()
#    print(best_game_stats)
    return render_template("statistics.html", user_stats=user_stats, best_game_stats=best_game_stats)

@app.route("/see_feedback")
def see_feedback():
    users.require_role(1)
    latest_five_feedbacks = data_statistics.latest_five_feedback_by_game()
    return render_template("see_feedback.html", latest_five_feedbacks=latest_five_feedbacks)

@app.route("/admin_feedback")
def admin_feedback():
    users.require_role(2)
    all_feedback = data_statistics.get_all_feedback()
    return render_template("admin_feedback.html", all_feedback=all_feedback)


@app.route("/admin_feedback_update", methods=["post"])
def admin_feedback_update():
#    print("admin feedback updateissa")
    users.require_role(2)
    users.check_ajax_csrf(request.json['session_id'])
    given_id = request.json['given_id']
    raw_new_text = request.json['new_text']
    raw_hidden_value = request.json['hidden_value']

    if len(raw_new_text) < 201:
        new_text = raw_new_text
    else: # see later if send an error message in this case or just use N/A
        new_text = "N/A"
    if raw_hidden_value > 1 or raw_hidden_value < 0:
        hidden_value = 0
    else: 
        hidden_value = raw_hidden_value

    data_statistics.admin_update_feedback(given_id, new_text, hidden_value)

    return ('', 200)

@app.route("/signout")
def signout():
    users.signout()
    return redirect("/")

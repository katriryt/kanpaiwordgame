from flask.templating import render_template
from db import db
from flask import session, abort, request
from werkzeug.security import check_password_hash, generate_password_hash
import os
from datetime import date, datetime
from pytz import timezone

def get_list_of_user_names():
    sql = "SELECT name FROM users"
    usernames_raw = db.session.execute(sql).fetchall()
    names_in_database = []
    for name in usernames_raw:
        names_in_database.append(name[0])
    return names_in_database

def check_user_name_exists(name):
    given_user_name = name
    names_in_database = get_list_of_user_names()
    if given_user_name not in names_in_database:
        return True
    else:
        return False

def signup(name, password, role):
    # This method creates a new user with password and role in the database
    hashvalue = generate_password_hash(password)
    try:
        sql = """INSERT INTO users (name, password, role) 
                VALUES(:name, :password, :role)"""
        db.session.execute(sql, {"name":name, "password":hashvalue, "role":role}) 
        db.session.commit()

    except Exception as e:
#        print(e)
        return False

#    print("signup ok")
    return signin(name, password)

def signin(given_name, given_password):
    sql = """SELECT id, name, password, role FROM users WHERE name=:name"""
    result = db.session.execute(sql, {"name":given_name}).fetchone()

    if check_password_hash(result[2], given_password):
#        print("tehdään sessio")
        session["user_id"] = result[0]
        session["user_name"] = given_name
        session["user_role"] = result[3]
        session["csrf_token"] = os.urandom(16).hex()
        utc = timezone('utc')
        temp = { 'gamename' : 'Adjectives', 'roundnumber' : 0, 'maxrounds' : 20, 'correctanswers' : 0, 'words_total' : 20, 'game_start_time' : datetime.now(utc), 'game_end_time' : None}
        session['gameinfo'] = temp
        session.modified = True
#        print(session)
#        print("signin ok")
#        print("tehdään merkintä session alkamisesta")
        save_session_start()
#        print("session saved")
        return True
    else:
        return False

def save_session_start(): # poista täältä player_id?
#    print("saving session start time")
    session_id = session["csrf_token"]
    player_id = session["user_id"]
#    now = datetime.now()
#    start_time = datetime.timestamp(now)
#    start_time = datetime.now()
#    print(session_id, player_id, start_time)
#    print(session_id, player_id)
    try:
        sql = """INSERT INTO sessions (session_id, player_id, start_time) VALUES (:session_id, :player_id, :start_time)"""
        db.session.execute(sql, {"session_id":session_id, "player_id":player_id, "start_time":'(NOW())'})
        db.session.commit()
    except Exception as e:
#        print("start time logging did not work")
        return False
    return True

def save_session_end():
#    print("saving session end time")
    session_id = session["csrf_token"]
#    print(session_id)
#    sql = """UPDATE sessions SET end_time = '(NOW())' WHERE session_id = session_id""" # toimii, kokeillaan turvallisuuden lisäämistä

    try:
        sql = """UPDATE sessions
                SET end_time=:end_time
                WHERE session_id=:session_id"""
    #    db.session.execute(sql) # toimi
        db.session.execute(sql, {"end_time":'(NOW())', "session_id":session_id})
        db.session.commit()
#        print("end time updated ok")
    except Exception as e:
#        print("end time update NOK")
        return False
    return True    

def signout():
#    print("signoutissa")
    save_session_end()
#    print("paluu onnistui")
    #del session["user_id"]
    #del session["user_name"]
    #del session["user_role"]
    session.clear()


def check_ajax_csrf(given_session_id):
#    print("csrf checkissa")
#    print(session)
#    print(session['csrf_token'])

    if session['csrf_token'] != given_session_id:
#        print("ajax csrf ei toiminut")
        abort(403)
#    print("ajax csrf toimi")

def check_form_csrf():
#    print("csrf checkissa")
#    print(session)
#    print(session['csrf_token'])

    if session['csrf_token'] != request.form["session_id"]:
#        print("csrf ei toiminut")
        abort(403)
#    print("csrf toimi")

def require_role(role):
#    print("vaatii roolia tasolta: ")
#    print(role)
#    print("käyttäjän rooli on: ")
#    print(session['user_role'])
    if role > session['user_role']:
#        print("vaadittu rooli ei täyttynyt")
        abort(403)
#    print("rooli ok")
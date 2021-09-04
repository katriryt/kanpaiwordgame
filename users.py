import os
from datetime import datetime
from flask import session, abort, request
from werkzeug.security import check_password_hash, generate_password_hash
from pytz import timezone
from db import db

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
    hashvalue = generate_password_hash(password)
    try:
        sql = """INSERT INTO users (name, password, role)
                VALUES(:name, :password, :role)"""
        db.session.execute(sql, {"name":name, "password":hashvalue, "role":role})
        db.session.commit()

    except Exception as e:
        print(e)
        return False

    return signin(name, password)

def signin(given_name, given_password):
    sql = """SELECT id, name, password, role FROM users WHERE name=:name"""
    result = db.session.execute(sql, {"name":given_name}).fetchone()

    if check_password_hash(result[2], given_password):
        session["user_id"] = result[0]
        session["user_name"] = given_name
        session["user_role"] = result[3]
        session["csrf_token"] = os.urandom(16).hex()
        utc = timezone('utc')
        temp = { 'gamename' : 'Adjectives', 'roundnumber' : 0,
                 'maxrounds' : 20, 'correctanswers' : 0,
                 'words_total' : 20, 'game_start_time' : datetime.now(utc),
                 'game_end_time' : None }
        session['gameinfo'] = temp
        session.modified = True
        save_session_start()
        return True
    else:
        return False

def save_session_start():
    session_id = session["csrf_token"]
    player_id = session["user_id"]
    try:
        sql = """INSERT INTO sessions (session_id, player_id, start_time)
                 VALUES (:session_id, :player_id, :start_time)"""
        db.session.execute(sql, { "session_id": session_id,
                                  "player_id": player_id,
                                  "start_time": '(NOW())' })
        db.session.commit()
    except Exception as e:
        print(e)
        return False
    return True

def save_session_end():
    session_id = session["csrf_token"]

    try:
        sql = """UPDATE sessions
                SET end_time=:end_time
                WHERE session_id=:session_id"""
        db.session.execute(sql, { "end_time": '(NOW())', "session_id": session_id })
        db.session.commit()
    except Exception as e:
        print(e)
        return False
    return True

def signout():
    save_session_end()
    session.clear()

def check_ajax_csrf(given_session_id):
    if session['csrf_token'] != given_session_id:
        abort(403)

def check_form_csrf():
    if session['csrf_token'] != request.form["session_id"]:
        abort(403)

def require_role(role):
    if role > session['user_role']:
        abort(403)

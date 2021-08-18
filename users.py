from flask.templating import render_template
from db import db
from flask import session, abort, request
from werkzeug.security import check_password_hash, generate_password_hash
import os

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
        session["user_id"] = result[0]
        session["user_name"] = given_name
        session["user_role"] = result[3]
        session["csrf_token"] = os.urandom(16).hex()
        temp = { 'gamename' : 'Adjectives', 'roundnumber' : 0, 'maxrounds' : 20, 'correctanswers' : 0, 'words_total' : 20} # Asetetaan täällä alkuperäinen pelin nimi
        session['gameinfo'] = temp
        print(session)
#        print("signin ok")
        return True
    else:
        return False

def signout():
#    print("signoutissa")
    #del session["user_id"]
    #del session["user_name"]
    #del session["user_role"]
    session.clear()

def check_csrf():
#    print("csrf checkissa")
#    print(session)
#    print(session['csrf_token'])

    if session['csrf_token'] != request.form["session_id"]:
        print("csrf ei toiminut")
        abort(403)
    print("csrf toimi")
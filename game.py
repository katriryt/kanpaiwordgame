from datetime import datetime
from flask import session
from pytz import timezone
from db import db

def save_feedback(game_class, player_id, session_id, points, comments):
    sql ="""INSERT INTO feedback (
            game_class,
            player_id,
            session_id,
            points,
            comments,
            hidden)
            VALUES (
                :game_class,
                :player_id,
                :session_id,
                :points,
                :comments,
                'false')
    """
    db.session.execute(sql,
                        { "game_class": game_class,
                          "player_id": player_id,
                          "session_id": session_id,
                          "points": points,
                          "comments": comments })
    db.session.commit()

def save_game_results(game_class, player_id, session_id, total_words,
                      words_correct, game_start_time, game_end_time):
    sql ="""INSERT INTO game_statistics (
            game_class,
            player_id,
            session_id,
            total_words,
            words_correct,
            game_start_time,
            game_end_time)
            VALUES (
                :game_class,
                :player_id,
                :session_id,
                :total_words,
                :words_correct,
                :game_start_time,
                :game_end_time)
    """
    db.session.execute(sql,
                         { "game_class": game_class,
                           "player_id": player_id,
                           "session_id": session_id,
                           "total_words": total_words,
                           "words_correct": words_correct,
                           "game_start_time": game_start_time,
                           "game_end_time": game_end_time})
    db.session.commit()

def get_total_word_count(given_gamename):
    sql = """SELECT class, count(*)
            FROM words
            WHERE class=:class
            GROUP BY class"""
    result = db.session.execute(sql, {"class":given_gamename}).fetchone()
    return result[1]

def restart_game(given_gamename):
    session['gameinfo']['gamename'] = given_gamename
    session['gameinfo']['correctanswers'] = 0
    session['gameinfo']['words_total'] = get_total_word_count(given_gamename)
    session['gameinfo']['maxrounds'] = session['gameinfo']['words_total']
    session['gameinfo']['roundnumber'] = 0
    utc = timezone('utc')
    session['gameinfo']['game_start_time'] = datetime.now(utc)
    session.modified = True

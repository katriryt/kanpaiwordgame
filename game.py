from db import db
from flask import session

def save_feedback(game_class, player_id, session_id, points, comments):
#    print("starting to save feedback")
#    print(game_class, player_id, session_id, points, comments)

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
    db.session.execute(sql, {"game_class":game_class, "player_id":player_id, "session_id":session_id, "points":points, "comments":comments})
    db.session.commit()

def save_game_results(game_class, player_id, session_id, total_words, words_correct):
#    print("starting to save game results")
#    print(game_class, player_id, session_id, total_words, words_correct)
    sql ="""INSERT INTO game_statistics (
            game_class, 
            player_id, 
            session_id, 
            total_words, 
            words_correct)
            VALUES (
                :game_class, 
                :player_id, 
                :session_id, 
                :total_words, 
                :words_correct)
    """
    db.session.execute(sql, {"game_class":game_class, "player_id":player_id, "session_id":session_id, "total_words":total_words, "words_correct":words_correct})
    db.session.commit()

def get_total_word_count(given_gamename):
#    print('wordcount')
#    print(given_gamename)
    sql = """SELECT class, count(*)
            FROM words
            WHERE class=:class
            GROUP BY class"""
    result = db.session.execute(sql, {"class":given_gamename}).fetchone()
#    print(result)
#    print(result[1])
    return result[1]

def restart_game(given_gamename):
#    print("restarting game, session info currently is...")
#    print(session)
    session['gameinfo']['gamename'] = given_gamename
    session['gameinfo']['correctanswers'] = 0
    session['gameinfo']['words_total'] = get_total_word_count(given_gamename)
    session['gameinfo']['maxrounds'] = session['gameinfo']['words_total']
    session['gameinfo']['roundnumber'] = 0
    session.modified = True
#    print("updates done, new session is...")
#    print(session)
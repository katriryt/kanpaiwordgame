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
            comments)
            VALUES (
                :game_class, 
                :player_id, 
                :session_id, 
                :points, 
                :comments)
    """
    db.session.execute(sql, {"game_class":game_class, "player_id":player_id, "session_id":session_id, "points":points, "comments":comments})
    db.session.commit()

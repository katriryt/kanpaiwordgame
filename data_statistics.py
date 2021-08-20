from db import db
from flask import session

def user_statistics(player_id): 
#    print("haetaan pelaajan statistiikkaa")
    sql = """SELECT game_class, 
                MAX(total_words) as total_words, 
                MAX(words_correct) as highest_correct,
                100*MAX(words_correct)/MAX(total_words) as best_rate,
                COUNT(session_id) as sessions_number, 
                CAST(AVG(words_correct) as int) as average_correct,
                CAST(100*AVG(words_correct)/MAX(total_words) as int) as average_rate
                FROM game_statistics
                WHERE player_id =:player_id 
                GROUP BY player_id, game_class
                ORDER BY game_class ASC"""
    player_stats = db.session.execute(sql, {"player_id":player_id}).fetchall()
#    print(player_stats)
    return player_stats

def best_game_statistics():
#    print("haetaan pelien statistiikkaa")
    sql = """SELECT Z.game_class, Z.times_played, Z.total_words, Z.highest_correct, Z.best_rate, U.name
                FROM
                (SELECT *
                    FROM (
                        SELECT X.*, ROW_NUMBER () OVER (PARTITION BY X.game_class ORDER BY X.highest_correct DESC) as playerposition
                            FROM(
                                SELECT 
                                    game_class, 
                                    player_id,
                                    COUNT(session_id) as times_played,
                                    MAX(total_words) as total_words, 
                                    MAX(words_correct) as highest_correct,
                                    100*MAX(words_correct)/MAX(total_words) as best_rate
                                    FROM game_statistics 
                                    GROUP BY game_class, player_id
                            ) as X
                            ) AS Y
                    WHERE Y.playerposition = 1
                ) as Z
                LEFT JOIN users as U ON U.id = Z.player_id
    """
    best_game_stats = db.session.execute(sql).fetchall()
#    print(best_game_stats)
    return best_game_stats

def latest_five_feedback_by_game():
#    print("haetaan viimeisimmät palautteet per peli")
    sql = """SELECT 
                game_class, 
                points, 
                comments 
                FROM(
                    SELECT 	game_class,
                            points, 
                            comments, 
                            ROW_NUMBER () OVER (PARTITION BY game_class ORDER BY id DESC) as latest_comments
                            FROM feedback 
                    ) AS Y
                    WHERE Y.latest_comments <= 5
                    ORDER BY game_class ASC
    """
    latest_five_by_class = db.session.execute(sql).fetchall()
#    print(latest_five_by_class)
    return latest_five_by_class
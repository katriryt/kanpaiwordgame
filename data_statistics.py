from db import db

def user_statistics(player_id):
    sql = """SELECT
                top_game.game_class,
                top_game.total_words,
                top_game.words_correct as highest_correct,
                top_game.success_rate as best_rate,
                top_game.duration as best_time,
                average_games.sessions_number,
                average_games.total_time_played as total_time_played,
                average_games.average_correct,
                average_games.average_rate
            FROM (
                SELECT
                    top_row.game_class,
                    top_row.total_words,
                    top_row.words_correct,
                    top_row.success_rate,
                    top_row.duration,
                    top_row.row_number
                FROM (
                    SELECT *,
                        ROW_NUMBER () OVER (PARTITION BY X.game_class ORDER BY X.words_correct DESC, X.duration ASC)
                    FROM (
                        SELECT *,
                            CAST(EXTRACT('EPOCH' FROM(game_end_time-game_start_time)) as int) as duration,
                            CAST((100*(words_correct::float/total_words::float)) as int) as success_rate
                        FROM game_statistics
                        WHERE player_id =:player_id
                        ORDER BY game_class ASC, words_correct DESC, duration ASC
                    ) as X
                ) as top_row
                WHERE top_row.row_number = 1
            ) as top_game
            LEFT JOIN (
                SELECT Y.game_class,
                COUNT(Y.id) as sessions_number,
                CAST(EXTRACT('EPOCH' FROM(SUM(Y.duration)))/60 as int) as total_time_played,
                CAST(AVG(Y.words_correct) as int) as average_correct,
                CAST(100*AVG(Y.words_correct)/MAX(Y.total_words) as int) as average_rate
                FROM (
                    SELECT *,
                        (game_end_time-game_start_time) as duration
                    FROM game_statistics
                ) as Y
                WHERE Y.player_id =:player_id
                GROUP BY Y.game_class
            ) as average_games ON top_game.game_class = average_games.game_class
    """
    player_stats = db.session.execute(sql,
                                    { "player_id": player_id,
                                      "Y.player_id": player_id }).fetchall()
    return player_stats

def best_game_statistics():
    sql = """SELECT B.game_class, C.times_played, C.total_time_mins,
                    B.total_words, B.words_correct, B.success_rate, B.name as best_player, B.duration_secs
            FROM(
                SELECT *
                FROM (
                    SELECT Z.game_class, Z. total_words, Z.words_correct, Z.success_rate, Z.duration_secs, Z.row_number, Z.player_id
                    FROM (
                        SELECT *,
                            ROW_NUMBER () OVER (PARTITION BY Y.game_class ORDER BY Y.words_correct DESC, Y.duration_secs ASC)
                        FROM(
                            SELECT *,
                                CAST((100*(words_correct::float/total_words::float)) as int) as success_rate,
                                CAST(EXTRACT('EPOCH' FROM(game_end_time-game_start_time)) as int) as duration_secs
                            FROM game_statistics
                            ORDER BY game_class ASC, words_correct DESC, duration_secs ASC
                        ) as Y
                    ) as Z
                    WHERE Z.row_number = 1
                ) as W
                LEFT JOIN (
                    SELECT id, name
                    FROM users
                    ) as A ON W.player_id = A.id
            ) as B
            LEFT JOIN (
                SELECT X.game_class,
                        COUNT(X.id) as times_played,
                        SUM(X.duration) as total_time,
                        CAST(EXTRACT('EPOCH' FROM (SUM(X.duration)))/60 as int) as total_time_mins
                FROM (
                    SELECT *, (game_end_time-game_start_time) as duration
                    FROM game_statistics
                ) as X
                GROUP BY X.game_class
                ORDER BY X.game_class ASC
            ) as C ON C.game_class = B.game_class
    """
    best_game_stats = db.session.execute(sql).fetchall()
    return best_game_stats

def heaviest_users():
    sql = """SELECT heavy_users.name, heavy_users.total_time_mins
        FROM(
            SELECT *
            FROM (
                SELECT Y.player_id, Y.total_time_mins
                FROM (
                    SELECT X.player_id,
                        SUM(X.visit_length) as total_time,
                        CAST(EXTRACT('EPOCH' FROM (SUM(X.visit_length)))/60 as int) as total_time_mins,
                        ROUND((EXTRACT('EPOCH' FROM (SUM(X.visit_length)))/3600)::numeric, 2)::float as total_time_hours
                    FROM (
                        SELECT *,
                            (end_time-start_time) as visit_length
                        FROM sessions
                        ORDER BY player_id
                    ) as X
                    GROUP BY X.player_id
                    ORDER BY total_time_mins DESC
                ) as Y
                WHERE Y.total_time_mins is NOT NULL
                LIMIT 5
            ) as Z
            LEFT JOIN (
                SELECT id, name
                FROM users
            ) as W ON Z.player_id = W.id
        ) as heavy_users
    """
    heaviest_users_raw = db.session.execute(sql).fetchall()
    heaviest_users_names = []
    heaviest_users_numbers = []
    for i in heaviest_users_raw:
        heaviest_users_names.append(i[0])
        heaviest_users_numbers.append(i[1])
    heaviest_users_ret = [heaviest_users_names, heaviest_users_numbers]
    return heaviest_users_ret

def most_frequent_players():
    sql = """SELECT Z.name, Z.number_games_played
            FROM (
                SELECT *
                FROM (
                    SELECT
                        player_id,
                        COUNT(id) as number_games_played
                    FROM game_Statistics
                    GROUP BY player_id
                    ORDER BY COUNT(id) DESC
                    LIMIT 5
                ) as X
                LEFT JOIN (
                    SELECT id, name
                    FROM users
                    ) as Y ON X.player_id = Y.id
            ) as Z
    """
    frequent_players_raw = db.session.execute(sql).fetchall()
    frequent_player_names = []
    frequency_games_played = []
    for i in frequent_players_raw:
        frequent_player_names.append(i[0])
        frequency_games_played.append(i[1])
    frequent_players = [frequent_player_names, frequency_games_played]
    return frequent_players

def latest_five_feedback_by_game():
    sql = """SELECT
                game_class,
                points,
                comments,
                response
                FROM(
                    SELECT 	game_class,
                            points,
                            comments,
                            response,
                            ROW_NUMBER () OVER (PARTITION BY game_class ORDER BY id DESC) as latest_comments
                            FROM feedback
                            WHERE hidden = '0'
                    ) AS Y
                    WHERE Y.latest_comments <= 5
                    ORDER BY game_class ASC
    """
    latest_five_by_class = db.session.execute(sql).fetchall()
    return latest_five_by_class

def get_all_feedback():
    sql = """SELECT Z.id as feedback_id,
                    Z.game_class as game_name,
                    Z.user_name as player_name,
                    Z.feedback_date as feedback_date,
                    Z.points as stars,
                    Z.hidden as hidden,
                    Z.comments,
                    Z.response
            FROM (
                SELECT *
                FROM feedback as C
                LEFT JOIN (
                    SELECT A.session_id, A.player_id, A.start_time, start_time:: timestamp ::date as feedback_date, B.user_id, B.user_name
                    FROM sessions as A
                    LEFT JOIN (
                        SELECT id as user_id,
                                name as user_name
                        FROM users
                    ) as B ON A.player_id = B.user_id
                ) as D on C.session_id = D.session_id
            ) as Z
            ORDER BY Z.id DESC
    """
    all_feedback = db.session.execute(sql).fetchall()
    return all_feedback

def admin_update_feedback(given_id, new_text, hidden_value):
    try:
        sql = """UPDATE feedback
            SET response = :new_text,
	        hidden = :hidden_value
            WHERE id = :given_id;
        """
        db.session.execute(sql,
                            { "new_text": new_text,
                              "hidden_value": hidden_value,
                              "given_id": given_id})
        db.session.commit()
    except Exception as e:
        print(e)
        return False
    return True

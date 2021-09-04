import random
from flask import session
from db import db

def get_game_names():
    sql = "SELECT class FROM words GROUP BY class"
    game_names_raw = db.session.execute(sql).fetchall()
    game_names = []
    for name in game_names_raw:
        game_names.append(name[0])
    game_names.sort()
    return game_names

def one_series_get_all(wanted_class):
    sql = "SELECT * FROM words WHERE class=:class"
    one_series_data_raw = db.session.execute(sql, {"class":wanted_class}).fetchall()
    return one_series_data_raw

def one_series_game_cards():
    temp = session['gameinfo']
    given_wanted_class = temp['gamename']
    one_series_data_raw = one_series_get_all(given_wanted_class)

    all_english_options = []
    for word_row in one_series_data_raw:
        all_english_options.append(word_row.english)

    one_series_full_game = []
    for word_row in one_series_data_raw:
        input_to_one_game = []
        input_to_one_game.append(word_row.id)
        input_to_one_game.append(word_row.kanji)
        input_to_one_game.append(word_row.hiragana)
        input_to_one_game.append(word_row.roomaji)
        input_to_one_game.append(word_row.english)

        answer_alternatives = []
        answer_alternatives = random.sample(set(all_english_options), 4)
        if word_row.english not in answer_alternatives:
            answer_alternatives.pop()
            answer_alternatives.append(word_row.english)

        answer_alternatives.sort()

        input_to_one_game.append(answer_alternatives)
        one_series_full_game.append(input_to_one_game)

    return one_series_full_game

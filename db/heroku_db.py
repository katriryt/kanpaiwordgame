import pandas as pd
from os import getenv
import sqlalchemy

heroku_secret_key = getenv('HEROKU_LINK')
db = sqlalchemy.create_engine(heroku_secret_key)

sql_1 = """CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    password TEXT,
    role INTEGER
);"""

db.execute(sql_1)
sql_2 = """CREATE TABLE words(
    id SERIAL PRIMARY KEY,
    class TEXT,
    kanji TEXT, 
    hiragana TEXT,
    roomaji TEXT,
    english TEXT
);"""

db.execute(sql_2)

input_data = pd.read_csv('words.csv', delimiter=',')

input_data.to_sql('words', db, if_exists='append', index=False)


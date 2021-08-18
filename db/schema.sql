CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    password TEXT,
    role INTEGER
);

CREATE TABLE words(
    id SERIAL PRIMARY KEY,
    class TEXT,
    kanji TEXT, 
    hiragana TEXT,
    roomaji TEXT,
    english TEXT
);

CREATE TABLE game_statistics(
    id SERIAL PRIMARY KEY,
    game_class TEXT,
    player_id INTEGER REFERENCES users (id),
    session_id TEXT, 
    total_words INTEGER,
    words_correct INTEGER
);

CREATE TABLE feedback(
    id SERIAL PRIMARY KEY,
    game_class TEXT, 
    player_id INTEGER REFERENCES users (id),
    session_id TEXT,
    points INTEGER, 
    comments TEXT
);
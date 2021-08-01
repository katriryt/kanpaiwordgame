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
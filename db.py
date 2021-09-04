from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv

#print("db.py sivulla")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("database")
db = SQLAlchemy(app)

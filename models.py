from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    hash = db.Column(db.String, nullable=False)

class Recipe(db.Model):
    __tablename__ = "recipes"
    recipe_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String, nullable=False)
    ingredients = db.Column(db.String, nullable=False)
    directions = db.Column(db.String, nullable=False)
    keywords = db.Column(db.String, nullable=False)
    vega = db.Column(db.Boolean, nullable=False)
    time = db.Column(db.String, nullable=True)
    image = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)

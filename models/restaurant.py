from flask_sqlalchemy import SQLAlchemy
from .restaurantOwner import RestaurantOwner

db = SQLAlchemy()

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    cuisine = db.Column(db.String(255), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('restaurant_owner.id'), nullable=False)
    owner = db.relationship('RestaurantOwner', backref=db.backref('restaurants', lazy=True))

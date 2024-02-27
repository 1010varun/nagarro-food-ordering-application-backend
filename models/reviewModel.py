from flask_sqlalchemy import SQLAlchemy
from .customer import Customer
from .restaurant import Restaurant
from .menu import Menu

db = SQLAlchemy()

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    customer = db.relationship('Customer', backref=db.backref('reviews', lazy=True))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    restaurant = db.relationship('Restaurant', backref=db.backref('reviews', lazy=True))
    dish_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=False)
    dish = db.relationship('Menu', backref=db.backref('reviews', lazy=True))
    rating = db.Column(db.Float, nullable=False)
    review_text = db.Column(db.Text)

from flask_sqlalchemy import SQLAlchemy
from .customer import Customer
from .restaurant import Restaurant

db = SQLAlchemy()

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    customer = db.relationship('Customer', backref=db.backref('orders', lazy=True))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    restaurant = db.relationship('Restaurant', backref=db.backref('orders', lazy=True))
    date_time = db.Column(db.DateTime, nullable=False)
    order_status = db.Column(db.String(20), nullable=False)

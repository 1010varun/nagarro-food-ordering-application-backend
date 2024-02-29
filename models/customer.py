from config.dbconfig import db
from json import loads, dumps

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="Customer")
    cart = db.Column(db.Text, default=dumps([]))
    orders = db.relationship('Order', backref='customer', lazy=True)


    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone_number': self.phone_number,
            'role': self.role,
            'cart': loads(self.cart),
            'orders': [order.serialize() for order in self.orders]
        }

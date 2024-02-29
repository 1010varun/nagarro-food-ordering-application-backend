from config.dbconfig import db
from .customer import Customer
from .restaurant import Restaurant
from json import dumps, loads


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    order_status = db.Column(db.String(20), nullable=False)
    items = db.Column(db.Text)

    def serialize(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'status': self.order_status,
            'items': [item for item in loads(self.items)]
        }

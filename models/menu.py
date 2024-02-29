from config.dbconfig import db
from .restaurant import Restaurant

class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    restaurant = db.relationship('Restaurant', backref=db.backref('menu_items', lazy=True))
    dish_name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)

    def serialize(self):
        return {
            'id': self.id,
            'restaurant_id': self.restaurant_id,
            'dish_name': self.dish_name,
            'price': self.price,
            'description': self.description
        }

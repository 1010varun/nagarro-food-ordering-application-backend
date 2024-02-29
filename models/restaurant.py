from config.dbconfig import db
from .restaurantOwner import RestaurantOwner


class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    cuisine = db.Column(db.String(255), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('restaurant_owner.id'), nullable=False)
    # owner = db.relationship('RestaurantOwner', backref=db.backref('restaurants', lazy=True))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'cuisine': self.cuisine,
            'owner_id': self.owner_id
        }
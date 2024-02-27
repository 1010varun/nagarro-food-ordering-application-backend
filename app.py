from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


from models.customer import Customer
from models.restaurant import Restaurant
from models.restaurantOwner import RestaurantOwner
from models.menu import Menu
from models.order import Order
from models.reviewModel import Review
from models.admin import Admin



with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)

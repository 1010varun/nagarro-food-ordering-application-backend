from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config.dbconfig import db
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta

from routes.customer import customer_routes
from routes.restaurant import restaurant_routes


from models.customer import Customer
from models.restaurant import Restaurant
from models.restaurantOwner import RestaurantOwner
from models.menu import Menu
from models.order import Order
from models.reviewModel import Review
from models.admin import Admin


app = Flask(__name__)
CORS(app, origins="*")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = "sample secret key"
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=90)
jwt = JWTManager(app)


db.init_app(app)


app.register_blueprint(customer_routes, url_prefix="/customer")
app.register_blueprint(restaurant_routes, url_prefix="/restaurant")



try:
    with app.app_context():
        db.create_all()
        print("tables created successfully")

except: 
    print("error occured while creating tables")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)

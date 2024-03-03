from models.restaurant import Restaurant
from models.customer import Customer
from models.menu import Menu
from models.order import Order
from flask import jsonify, abort
from config.dbconfig import db
from json import dumps, loads
from datetime import datetime
from flask_jwt_extended import create_access_token


def register_customer(name, email, phone_number, password):
    existing_customer = Customer.query.filter_by(email=email).first()
    
    if existing_customer:
        abort(400, "Customer with this email already exists. Please use a different email.")

    new_customer = Customer(name=name, email=email, phone_number=phone_number, password=password)
    db.session.add(new_customer)
    db.session.commit()
    
    return new_customer


def customer_login(email, password):
    customer = Customer.query.filter_by(email=email).first()

    if not customer or not customer.check_password(password):
        abort(401, "Invalid email or password")

    access_token = create_access_token(identity=email)

    return jsonify({"message": "Customer login successful", "token": access_token})


def get_customer_by_id(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        abort(404, f"Customer with ID {customer_id} not found")
    return customer


def add_to_cart(customer_id, dish_id):
    customer = get_customer_by_id(customer_id)
    cart = loads(customer.cart)
    cart.append(dish_id)
    customer.cart = dumps(cart)
    db.session.commit()

    return customer.cart


def place_order(customer_id):
    customer = get_customer_by_id(customer_id)
    
    cart = loads(customer.cart)

    if not len(cart):
        abort(400, "Cart is empty. Add items to the cart before placing an order.")

    cart_items = cart

    items_by_restaurant = {}
    for dish_id in cart_items:
        menu_item = Menu.query.get(dish_id)
        if menu_item:
            restaurant_id = menu_item.restaurant_id
            if restaurant_id not in items_by_restaurant:
                items_by_restaurant[restaurant_id] = []
            items_by_restaurant[restaurant_id].append(dish_id)

    for restaurant_id, items in items_by_restaurant.items():
        order = Order(
            customer=customer,
            restaurant_id=restaurant_id,
            date_time=datetime.utcnow(),
            order_status="Placed",
            items=dumps(items)
        )
        db.session.add(order)

    cart = []
    customer.cart = dumps(cart)
    db.session.commit()

    return jsonify({"message": "Orders placed successfully"})


def view_order_history(customer_id):
    customer = get_customer_by_id(customer_id)
    orders = Order.query.filter_by(customer_id=customer.id).all()
    return orders


def browse_restaurants(location=None, cuisine=None, name=None):
    query = Restaurant.query
    if location:
        query = query.filter(Restaurant.location.ilike(f'%{location}%'))
    if cuisine:
        query = query.filter(Restaurant.cuisine.ilike(f'%{cuisine}%'))
    if name:
        query = query.filter(Restaurant.name.ilike(f'%{name}%'))
    restaurants = query.all()
    return restaurants


def view_menu(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)
    
    if not restaurant:
        return(f"Restaurant with ID {restaurant_id} not found")

    menu_items = Menu.query.filter_by(restaurant_id=restaurant_id).all()

    return{
        "restaurant_name": restaurant.name,
        "location": restaurant.location,
        "cuisine": restaurant.cuisine,
        "menu": [{"dish_name": item.dish_name, "price": item.price, "description": item.description} for item in menu_items]
    }
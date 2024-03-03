from flask import Blueprint, jsonify, request
from services.customer import *
from flask_jwt_extended import jwt_required

customer_routes = Blueprint('customer_routes', __name__)


@customer_routes.route('/getrestaurants', methods=['GET'])
@jwt_required()
def browse_and_search_restaurants():
    location = request.args.get('location')
    cuisine = request.args.get('cuisine')
    name = request.args.get('name')
    restaurants = browse_restaurants(location=location, cuisine=cuisine, name=name)
    return jsonify([restaurant.serialize() for restaurant in restaurants])


@customer_routes.route('/viewmenu/<int:restaurant_id>', methods=['GET'])
@jwt_required()
def customer_view_menu(restaurant_id):
    menu_info = view_menu(restaurant_id)
    return jsonify(menu_info)


@customer_routes.route('/registercustomer', methods=['POST'])
@jwt_required()
def register_customer_route():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone_number = data.get('phone_number')
    password = data.get('password')

    if not name or not email or not phone_number or not password:
        abort(400, "Incomplete data. Please provide name, email, phone number, and password.")

    customer = register_customer(name, email, phone_number, password)

    return jsonify(customer.serialize()), 201


@customer_routes.route('/addtocart/<int:customer_id>', methods=['POST'])
@jwt_required()
def add_to_cart_route(customer_id):
    data = request.get_json()
    dish_id = data.get('dish_id')
    
    cart = add_to_cart(customer_id, dish_id)
    
    return jsonify({"message": "Item added to cart successfully"})


@customer_routes.route('/placeorder/<int:customer_id>', methods=['POST'])
@jwt_required()
def place_order_route(customer_id):
    place_order(customer_id)
    
    return jsonify({"message": "Order placed successfully"})


@customer_routes.route('/orderhistory/<int:customer_id>', methods=['GET'])
@jwt_required()
def view_order_history_route(customer_id):
    orders = view_order_history(customer_id)
    
    return jsonify([order.serialize() for order in orders])

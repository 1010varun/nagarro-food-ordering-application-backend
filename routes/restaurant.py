from flask import Blueprint, jsonify, request
from services.restaurant import *
from json import loads
from flask_jwt_extended import jwt_required

restaurant_routes = Blueprint('restaurant_routes', __name__)


@restaurant_routes.route('/restaurant-owners/register', methods=['POST'])
def register_restaurant_owner_route():
    data = request.get_json()
    if not data.get('name') or not data.get('email') or not data.get('phone_number') or not data.get('password'):
        return jsonify({"error": "Missing required fields"}), 400

    owner = register_restaurant_owner(data)

    return jsonify({"message": "Restaurant owner registered successfully", "owner_id": owner.id})

@restaurant_routes.route('/login', methods=['POST'])
def restaurant_owner_login_route():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    return restaurant_owner_login(email, password)


@restaurant_routes.route('/restaurant-owners/<int:owner_id>', methods=['GET'])
def get_restaurant_owner(owner_id):
    owner = get_restaurant_owner_by_id(owner_id)
    return jsonify(owner.serialize())


@restaurant_routes.route('/restaurant-owners/<int:owner_id>/register-restaurant', methods=['POST'])
def register_new_restaurant(owner_id):
    data = request.get_json()
    restaurant = register_restaurant(owner_id, data)
    return jsonify(restaurant.serialize())


@restaurant_routes.route('/restaurants/<int:restaurant_id>/add-menu-item', methods=['POST'])
@jwt_required()
def add_menu_item_route(restaurant_id):
    data = request.get_json()
    dish_name = data.get('dish_name')
    price = data.get('price')
    description = data.get('description')

    if not dish_name or not price:
        abort(400, "Incomplete data. Please provide dish_name and price.")

    menu_item = add_menu_item(restaurant_id, dish_name, price, description)
    return jsonify(menu_item.serialize()), 201


@restaurant_routes.route('/menu/<int:menu_id>/edit', methods=['PUT'])
@jwt_required()
def edit_menu_item_route(menu_id):
    data = request.get_json()
    dish_name = data.get('dish_name')
    price = data.get('price')
    description = data.get('description')

    menu_item = edit_menu_item(menu_id, dish_name, price, description)
    return jsonify(menu_item.serialize())


@restaurant_routes.route('/menu/<int:menu_id>/delete', methods=['DELETE'])
@jwt_required()
def delete_menu_item_route(menu_id):
    result = delete_menu_item(menu_id)
    return jsonify(result)


@restaurant_routes.route('/orders/<int:restaurant_id>/orders', methods=['GET'])
@jwt_required()
def get_orders_for_restaurant_route(restaurant_id):
    orders = get_orders_for_restaurant(restaurant_id)
    return jsonify({"orders": loads(order.items) for order in orders})
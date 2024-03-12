from models.restaurant import Restaurant
from models.restaurantOwner import RestaurantOwner
from models.menu import Menu
from models.order import Order
from flask import jsonify, abort
from config.dbconfig import db
from flask_jwt_extended import create_access_token


def get_restaurant_owner_by_id(owner_id):
    owner = RestaurantOwner.query.get(owner_id)
    if not owner:
        abort(404, f"Restaurant Owner with ID {owner_id} not found")
    return owner


def restaurant_owner_login(email, password):
    owner = RestaurantOwner.query.filter_by(email=email).first()
    if not owner or not owner.check_password(password):
        abort(401, "Invalid email or password")
    access_token = create_access_token(identity=email)
    return jsonify({"message": "Restaurant owner login successful", "token": access_token, "role": owner.role, "email": email, "name": owner.name})


def register_restaurant(owner_id, restaurant_data):
    owner = get_restaurant_owner_by_id(owner_id)
    restaurant = Restaurant(**restaurant_data, owner=owner)
    db.session.add(restaurant)
    db.session.commit()
    return restaurant

def get_restaurant_by_id(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)
    if not restaurant:
        abort(404, f"Restaurant with ID {restaurant_id} not found")
    return restaurant

def register_restaurant_owner(owner_data):
    owner = RestaurantOwner(**owner_data)
    db.session.add(owner)
    db.session.commit()
    return owner

def add_menu_item(restaurant_id, dish_name, price, description):
    new_menu_item = Menu(restaurant_id=restaurant_id, dish_name=dish_name, price=price, description=description)
    db.session.add(new_menu_item)
    db.session.commit()
    return new_menu_item

def edit_menu_item(menu_id, dish_name, price, description):
    menu_item = Menu.query.get(menu_id)
    if not menu_item:
        abort(404, f"Menu item with ID {menu_id} not found")

    menu_item.dish_name = dish_name
    menu_item.price = price
    menu_item.description = description
    db.session.commit()
    return menu_item

def delete_menu_item(menu_id):
    menu_item = Menu.query.get(menu_id)
    if not menu_item:
        abort(404, f"Menu item with ID {menu_id} not found")

    db.session.delete(menu_item)
    db.session.commit()
    return {"message": f"Menu item with ID {menu_id} deleted successfully"}

def get_orders_for_restaurant(restaurant_id):
    orders = Order.query.filter_by(restaurant_id=restaurant_id).all()
    return orders

from flask import Blueprint, jsonify, request

from restaurant_service import RestaurantService
from order_service import OrderService
from review_service import ReviewService


owner_bp = Blueprint("owner", __name__)

restaurant_service = RestaurantService()
order_service = OrderService()
review_service = ReviewService()

@owner_bp.route("/restaurants", methods=["GET"])
def get_restaurants():
    try:
        restaurants = restaurant_service.get_all_restaurants()
        return jsonify(restaurants), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@owner_bp.route("/restaurants", methods=["POST"])
def register_restaurant():
    restaurant_data = request.json
    try:
        restaurant_id = restaurant_service.register_restaurant(restaurant_data)
        return jsonify({"restaurant_id": restaurant_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@owner_bp.route("/restaurants/<int:restaurant_id>/menu", methods=["POST"])
def add_menu_item(restaurant_id):
    menu_item_data = request.json
    try:
        menu_item_id = restaurant_service.add_menu_item(restaurant_id, menu_item_data)
        return jsonify({"menu_item_id": menu_item_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@owner_bp.route("/restaurants/<int:restaurant_id>/menu/<int:menu_item_id>", methods=["PUT"])
def edit_menu_item(restaurant_id, menu_item_id):
    updated_menu_item_data = request.json
    try:
        restaurant_service.edit_menu_item(restaurant_id, menu_item_id, updated_menu_item_data)
        return jsonify({"message": "Menu item updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@owner_bp.route("/restaurants/<int:restaurant_id>/menu/<int:menu_item_id>", methods=["DELETE"])
def delete_menu_item(restaurant_id, menu_item_id):
    try:
        restaurant_service.delete_menu_item(restaurant_id, menu_item_id)
        return jsonify({"message": "Menu item deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@owner_bp.route("/restaurants/<int:restaurant_id>/orders", methods=["GET"])
def get_orders(restaurant_id):
    try:
        orders = order_service.get_orders_for_restaurant(restaurant_id)
        return jsonify(orders), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@owner_bp.route("/restaurants/<int:restaurant_id>/reviews", methods=["GET"])
def get_reviews(restaurant_id):
    try:
        reviews = review_service.get_reviews_for_restaurant(restaurant_id)
        return jsonify(reviews), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

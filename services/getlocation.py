from com.yourapp.models import Restaurant, MenuItem, Order
from com.yourapp.database import db

class CustomerService:
    def search_restaurants(self, location=None, cuisine=None, restaurant_name=None):
        query = Restaurant.query
        if location:
            query = query.filter_by(location=location)
        if cuisine:
            query = query.filter_by(cuisine=cuisine)
        if restaurant_name:
            query = query.filter(Restaurant.name.ilike(f"%{restaurant_name}%"))
        restaurants = query.all()
        return restaurants

    def get_menu(self, restaurant_id):
        menu = MenuItem.query.filter_by(restaurant_id=restaurant_id).all()
        return menu

    def add_to_cart(self, item_id, quantity, user_id):
        cart_item = CartItem(item_id=item_id, quantity=quantity, user_id=user_id)
        db.session.add(cart_item)
        db.session.commit()
        return cart_item.order_id

    def place_order(self, items, user_id):
        order = Order(user_id=user_id)
        for item_id, quantity in items.items():
            order_item = OrderItem(item_id=item_id, quantity=quantity)
            order.items.append(order_item)
        db.session.add(order)
        db.session.commit()
        return order.id

    def track_order(self, order_id):
        order = Order.query.get(order_id)
        if order:
            return order.status
        return None

    def get_order_history(self, user_id):
        orders = Order.query.filter_by(user_id=user_id).all()
        return orders

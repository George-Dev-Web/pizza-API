from flask import Blueprint, request, jsonify
from server.models.restaurant_pizza import RestaurantPizza
from server.models.pizza import Pizza
from server.models.restaurant import Restaurant
from server.app import db

restaurant_pizza_bp = Blueprint('restaurant_pizza_bp', __name__, url_prefix='/restaurant_pizzas')

# ✅ Link pizza to restaurant
@restaurant_pizza_bp.route('/', methods=['POST'])
def create_restaurant_pizza():
    try:
        data = request.get_json()
        price = data.get('price')
        pizza_id = data.get('pizza_id')
        restaurant_id = data.get('restaurant_id')

        if price is None or not pizza_id or not restaurant_id:
            return jsonify({"error": "Missing fields"}), 400

        if not (1 <= price <= 30):
            return jsonify({"error": "Price must be between 1 and 30"}), 400

        pizza = Pizza.query.get(pizza_id)
        restaurant = Restaurant.query.get(restaurant_id)

        if not pizza or not restaurant:
            return jsonify({"error": "Invalid pizza or restaurant ID"}), 404

        link = RestaurantPizza(price=price, pizza_id=pizza_id, restaurant_id=restaurant_id)
        db.session.add(link)
        db.session.commit()

        return jsonify({
            "id": pizza.id,
            "name": pizza.name,
            "ingredients": pizza.ingredients
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ (Optional) List all links
@restaurant_pizza_bp.route('/', methods=['GET'])
def list_restaurant_pizzas():
    links = RestaurantPizza.query.all()
    result = [
        {
            "id": link.id,
            "price": link.price,
            "pizza_id": link.pizza_id,
            "restaurant_id": link.restaurant_id
        } for link in links
    ]
    return jsonify(result), 200

# ✅ Delete link by ID
@restaurant_pizza_bp.route('/<int:id>', methods=['DELETE'])
def delete_restaurant_pizza(id):
    link = RestaurantPizza.query.get(id)
    if not link:
        return jsonify({"error": "Link not found"}), 404

    db.session.delete(link)
    db.session.commit()
    return '', 204

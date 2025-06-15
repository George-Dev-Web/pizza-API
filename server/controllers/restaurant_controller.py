from flask import Blueprint, jsonify, request
from server.models.restaurant import Restaurant
from server.app import db

restaurant_bp = Blueprint('restaurant_bp', __name__, url_prefix='/restaurants')

# Get all restaurants
@restaurant_bp.route('/', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    result = [
        {
            "id": r.id,
            "name": r.name,
            "address": r.address
        } for r in restaurants
    ]
    return jsonify(result), 200

# Get one restaurant with its pizzas
@restaurant_bp.route('/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404

    result = {
        "id": restaurant.id,
        "name": restaurant.name,
        "address": restaurant.address,
        "pizzas": [
            {
                "id": rp.pizza.id,
                "name": rp.pizza.name,
                "ingredients": rp.pizza.ingredients,
                "price": rp.price
            } for rp in restaurant.pizzas
        ]
    }
    return jsonify(result), 200

#  Create a restaurant
@restaurant_bp.route('/', methods=['POST'])
def create_restaurant():
    data = request.get_json()
    name = data.get("name")
    address = data.get("address")

    if not name or not address:
        return jsonify({"error": "Name and address required"}), 400

    restaurant = Restaurant(name=name, address=address)
    db.session.add(restaurant)
    db.session.commit()

    return jsonify({
        "id": restaurant.id,
        "name": restaurant.name,
        "address": restaurant.address
    }), 201

# Delete a restaurant
@restaurant_bp.route('/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404

    db.session.delete(restaurant)
    db.session.commit()

    return '', 204

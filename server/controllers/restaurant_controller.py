from flask import Blueprint, jsonify, request
from server.models.restaurant import Restaurant
from server.models.restaurant_pizza import RestaurantPizza
from server.models import db

restaurant_bp = Blueprint('restaurant_bp', __name__)

# GET /restaurants
@restaurant_bp.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([restaurant.to_dict() for restaurant in restaurants]), 200


# GET /restaurants/<id>
@restaurant_bp.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        return jsonify(restaurant.to_dict(include_pizzas=True)), 200
    return jsonify({"error": "Restaurant not found"}), 404


# DELETE /restaurants/<id>
@restaurant_bp.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        return '', 204
    return jsonify({"error": "Restaurant not found"}), 404

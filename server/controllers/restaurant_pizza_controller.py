from flask import Blueprint, request, jsonify
from server.models.restaurant_pizza import RestaurantPizza
from server.models.pizza import Pizza
from server.models.restaurant import Restaurant
from server import db

restaurant_pizza_bp = Blueprint('restaurant_pizza_bp', __name__)

# POST /restaurant_pizzas
@restaurant_pizza_bp.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()

    price = data.get('price')
    pizza_id = data.get('pizza_id')
    restaurant_id = data.get('restaurant_id')

    if not price or not pizza_id or not restaurant_id:
        return jsonify({"errors": ["Missing fields"]}), 400

    if not (1 <= price <= 30):
        return jsonify({"errors": ["Price must be between 1 and 30"]}), 400

    pizza = Pizza.query.get(pizza_id)
    restaurant = Restaurant.query.get(restaurant_id)

    if not pizza or not restaurant:
        return jsonify({"errors": ["Invalid pizza or restaurant ID"]}), 400

    restaurant_pizza = RestaurantPizza(
        price=price,
        pizza_id=pizza_id,
        restaurant_id=restaurant_id
    )

    db.session.add(restaurant_pizza)
    db.session.commit()

    response = {
        "id": restaurant_pizza.id,
        "price": restaurant_pizza.price,
        "pizza_id": pizza.id,
        "restaurant_id": restaurant.id,
        "pizza": pizza.to_dict(),
        "restaurant": restaurant.to_dict()
    }

    return jsonify(response), 201

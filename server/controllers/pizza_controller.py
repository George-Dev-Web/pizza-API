from flask import Blueprint, request, jsonify
from server.models.pizza import Pizza
from server.app import db
import logging

pizza_bp = Blueprint('pizza_bp', __name__, url_prefix='/pizzas')


@pizza_bp.route('/', methods=['POST'])
def create_pizza():
    try:
        data = request.get_json()
        logging.debug(f"Incoming data: {data}")

        name = data.get('name')
        ingredients = data.get('ingredients')

        if not name or not ingredients:
            return jsonify({"error": "Name and ingredients are required"}), 400

        pizza = Pizza(name=name, ingredients=ingredients)
        db.session.add(pizza)
        db.session.commit()

        return jsonify({
            "id": pizza.id,
            "name": pizza.name,
            "ingredients": pizza.ingredients
        }), 201

    except Exception as e:
        logging.error(f"Error creating pizza: {e}")
        return jsonify({"error": "Internal server error"}), 500

#  GET route: list all pizzas
@pizza_bp.route('/', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    pizza_list = [
        {
            "id": pizza.id,
            "name": pizza.name,
            "ingredients": pizza.ingredients
        }
        for pizza in pizzas
    ]
    return jsonify(pizza_list), 200

# DELETE route: delete a pizza by ID
@pizza_bp.route('/<int:id>', methods=['DELETE'])
def delete_pizza(id):
    pizza = Pizza.query.get(id)
    if not pizza:
        return jsonify({"error": "Pizza not found"}), 404

    db.session.delete(pizza)
    db.session.commit()

    return jsonify({"message": f"Pizza with ID {id} deleted."}), 200

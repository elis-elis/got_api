"""
Pydantic's validation is just for input data (e.g., when you send data to your API),
but it doesn't directly interact with your database.
That's why I am using this schema to validate incoming data before inserting it into the database.
"""

from flask import Blueprint, request, jsonify
from app import db
from flask_jwt_extended import jwt_required
from app.models import Character
from app.schemas import CharacterCreateSchema, CharacterResponseSchema
from pydantic import ValidationError

# Blueprint for authenticated routes
auth_protected_bp = Blueprint("auth_protected", __name__)
# Create a Blueprint
characters_bp = Blueprint("characters", __name__)


# Example of a protected route
@auth_protected_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    """
    Protected route that requires a valid JWT token in the Authorization header.
    """
    return jsonify(message="You have access to this protected route"), 200


@characters_bp.route("/characters", methods=["POST"])
def create_characters():
    try:
        # Validate and parse JSON request body
        data = CharacterCreateSchema(**request.get_json())

        # Create new Character instance
        character = Character(
            name=data.name,
            house=data.house_id,
            animal=data.animal,
            symbol=data.symbol,
            nickname=data.nickname,
            role=data.role,
            age=data.age,
            death=data.death,
            strength=data.strength_id
        )

        # Add character to DB
        db.session.add(character)
        db.session.commit()

        return jsonify(character.to_dict()), 201

    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

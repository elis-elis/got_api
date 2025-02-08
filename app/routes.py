"""
Pydantic's validation is just for input data (e.g., when you send data to your API),
but it doesn't directly interact with your database.
That's why I am using this schema to validate incoming data before inserting it into the database.
"""

from flask import Blueprint, request, jsonify
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Character
from app.schemas import CharacterCreateSchema
from pydantic import ValidationError

# Create a Blueprint for character-related routes
characters_bp = Blueprint("characters", __name__)


@characters_bp.route('/characters', methods=['POST'])
@jwt_required()  # This will ensure only authorized users can create characters
def create_character():
    """
    Endpoint to create a new character. This route is protected by JWT authentication.
    """
    # Get the user identity from the JWT
    current_user = get_jwt_identity()  # This will be the data stored in the token

    # Validate incoming data (this can be done with pydantic or any other schema validation method)
    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided"}), 400

    # Parse and create a new character
    try:
        character_data = CharacterCreateSchema(**data)
        character = Character(**character_data.dict())
        db.session.add(character)
        db.session.commit()

        return jsonify({"message": "Character created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error: {str(e)}"}), 400

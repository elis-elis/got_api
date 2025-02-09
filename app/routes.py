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
import random

# Create a Blueprint for character-related routes
characters_bp = Blueprint("characters", __name__)


@characters_bp.route('/characters/list', methods=['GET'])
@jwt_required(optional=True)  # Authenticated or non-authenticated users can access
def get_characters():
    """
    Fetch all characters with optional pagination.
    Query Parameters:
    - limit: Number of characters to return (default: 20)
    - skip: Number of characters to skip (default: 0)
    """
    try:
        limit = request.args.get('limit', type=int, default=20)
        skip = request.args.get('skip', type=int, default=0)

        if limit <= 0:
            return jsonify({"message": "Limit must be greater than 0."})

        # Fetch characters from the database
        characters_query = Character.query.offset(skip).limit(limit)

        characters = characters_query.all()

        # If no pagination, return 20 random characters
        if "limit" not in request.args and "skip" not in request.args:
            all_characters = Character.query.all()
            characters = random.sample(all_characters, min(len(all_characters), 20))

        # Convert characters to JSON
        characters_data = []
        for char in characters:
            character_info = {
                "id": char.id,
                "name": char.name,
                "house": char.house.name if char.house else None,
                "animal": char.animal,
                "symbol": char.symbol,
                "nickname": char.nickname,
                "role": char.role,
                "age": char.age,
                "death": char.death,
                "strength": char.strength.description if char.strength else None
            }
            characters_data.append(character_info)

        return jsonify({"characters": characters_data, "count": len(characters_data)}), 200
    except Exception as e:
        return jsonify({"message": f"Error fetching characters: {str(e)}"}), 500


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

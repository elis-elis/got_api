"""
Pydantic's validation is just for input data (e.g., when sending data to the API),
but it doesn't directly interact with the database.
To validate incoming data before inserting it into the database.
"""
from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Character
from app.schemas import CharacterCreateSchema
from pydantic import ValidationError
import random
from app.utils import is_valid_uuid
from app.filters import (
    get_pagination_params,
    get_filter_params,
    apply_filters,
    apply_sorting,
    get_sorting_params
)
from app.utils import add_character


# Create a Blueprint for character-related routes
characters_bp = Blueprint("characters", __name__)


@characters_bp.route('/characters/list', methods=['GET'])
@jwt_required(optional=True)  # Authenticated or non-authenticated users can access
def get_characters():
    """
    Fetch characters with filtering, sorting, and pagination.
    """
    filters = get_filter_params()

    start_query = Character.query

    # Apply filters to query
    query = apply_filters(start_query, filters)

    # Apply sorting
    sort_by, sort_order = get_sorting_params()
    query = apply_sorting(query, sort_by, sort_order)

    # Apply pagination
    limit, skip = get_pagination_params()

    # Fetch characters from the database with pagination
    characters = query.offset(skip).limit(limit).all()

    return jsonify({
        "characters": [char.to_dict() for char in characters],
        "count": len(characters)
    }), 200


@characters_bp.route('/characters/<id:character_id>', methods=['GET'])
@jwt_required(optional=True)
def get_character(character_id):
    """
    Fetch a single character by its unique ID.
    """
    character = Character.query.get(character_id)

    if not character:
        return jsonify({"message": "Character not found. but don't give up."}), 404

    return jsonify(character.to_dict()), 200


@characters_bp.route('/character', methods=['POST'])
@jwt_required()  # This will ensure only authorized users can create characters
def create_character():
    """
    Endpoint to create a new character and store it in 'characters.json'.
    Check if data is valid (Pydantic schema validation).
    Load existing characters from the 'characters.json' file.
    Add the new character to the in-memory list.
    Save the updated list back to the 'characters.json' file.
    Return success response.
    Consideration: The data is lost if the server is restarted. For more permanent storage, switch to a database.
    """
    # Get the user identity from the JWT
    current_user = get_jwt_identity()  # for authentication purpose, although not used here directly

    # Get JSON data from the request
    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided"}), 400

    # Create a new character
    # Use Pydantic to validate the incoming character data
    character_data = CharacterCreateSchema(**data)
    new_character = character_data.dict()

    saved_character = add_character(new_character)

    return jsonify({"message": "Character created successfully", "character": saved_character}), 201


# This route is designed to save new character(s) in database
@characters_bp.route('/new_character', methods=['POST'])
@jwt_required()
def create_character_for_db():
    """
    Endpoint to create a new character and save it to the database.
    """
    current_user = get_jwt_identity()

    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided"}), 400

    character_data = CharacterCreateSchema(**data)
    character = Character(**character_data.dict())
    db.session.add(character)
    db.session.commit()

    return jsonify({"message": "Character created successfully"}), 201

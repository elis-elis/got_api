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

# Create a Blueprint for character-related routes
characters_bp = Blueprint("characters", __name__)


@characters_bp.route('/characters/list', methods=['GET'])
@jwt_required(optional=True)  # Authenticated or non-authenticated users can access
def get_characters():
    """
    Fetch characters with filtering, sorting, and pagination.
    """
    try:
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

    except ValueError:
        return jsonify({"message": "Invalid input. Limit and skip must be integers."}), 400

    except SQLAlchemyError as db_error:
        return jsonify({"message": f"Database error: {str(db_error)}"}), 500

    except Exception as e:
        return jsonify({"message": f"Unexpected error: {str(e)}"}), 500


@characters_bp.route('/characters/<string:character_id>', methods=['GET'])
@jwt_required(optional=True)
def get_character(character_id):
    """
    Fetch a single character by its unique ID.
    """
    try:
        if not character_id.isdigit() and not is_valid_uuid(character_id):
            return jsonify({"message": "Invalid character ID format"}), 400

        character = Character.query.get(character_id)

        if not character:
            return jsonify({"message": "Character not found. but don't give up."}), 404

        return jsonify(character.to_dict()), 200

    except SQLAlchemyError as db_error:
        return jsonify({"message": f"Database error: {str(db_error)}"}), 500  # Internal Server Error

    except Exception as e:
        return jsonify({"message": f"Unexpected error: {str(e)}"}), 500  # Catch-all for unknown issues


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
    except ValidationError as ve:
        return jsonify({"message": "Validation error", "errors": ve.errors()}), 400
    except SQLAlchemyError as db_error:
        db.session.rollback()
        return jsonify({"message": f"Database error: {str(db_error)}"}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Unexpected error: {str(e)}"}), 500

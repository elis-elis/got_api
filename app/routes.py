"""
Pydantic's validation is just for input data (e.g., when sending data to the API),
but it doesn't directly interact with the database.
To validate incoming data before inserting it into the database.
"""
from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from app import db, handle_404, handle_sqlalchemy_error, handle_500, handle_validation_error
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Character
from app.schemas import CharacterCreateSchema
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
def list_characters():
    """
    Fetch characters with filtering, sorting, and pagination.
    Returns both count (paginated result) & total (unpaginated count).
    """
    try:
        filters = get_filter_params()
        start_query = Character.query

        # Apply filters dynamically to query
        query = apply_filters(start_query, filters)

        # Get total count *before* pagination
        total_count = query.count()

        # Apply sorting
        sort_by, sort_order = get_sorting_params()
        query = apply_sorting(query, sort_by, sort_order)

        # Apply pagination
        limit, skip = get_pagination_params()

        # Fetch characters from the database with pagination
        characters = query.offset(skip).limit(limit).all()

        return jsonify({
            "characters": [character.to_dict() for character in characters],
            "count": len(characters),  # Number of characters returned after pagination
            "total": total_count  # Total number of characters before pagination
        }), 200

    except ValidationError as ve:
        return handle_validation_error(ve)

    except ValueError as e:
        return jsonify({"message": str(e)}), 400

    except Exception as e:
        return handle_500(e)


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
    try:
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

    except ValidationError as ve:
        return handle_validation_error(ve)

    except Exception as e:
        return handle_500(e)


# This route is designed to save new character(s) in database
@characters_bp.route('/new_character', methods=['POST'])
@jwt_required()
def create_character_for_db():
    """
    Endpoint to create a new character and save it to the database.
    """
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        if not data:
            return jsonify({"message": "No data provided"}), 400

        # Validate input
        character_data = CharacterCreateSchema(**data)
        character = Character(**character_data.dict())

        db.session.add(character)
        db.session.commit()

        return jsonify({"message": "Character created successfully"}), 201

    except ValidationError as ve:
        return handle_validation_error(ve)

    except SQLAlchemyError as db_error:
        db.session.rollback()
        return handle_sqlalchemy_error(db_error)

    except Exception as e:
        db.session.rollback()
        return handle_500(e)


@characters_bp.route('/characters/<int:character_id>', methods=['GET', 'PATCH', 'DELETE'])
@jwt_required()
def handle_character(character_id):
    """
    Handles fetching (GET), updating (PATCH), and deleting (DELETE) a character by ID.
    - GET: Returns the character details.
    - PATCH: Partially updates character fields.
    - DELETE: Removes the character from the database.
    """
    character = Character.query.get(character_id)
    if not character:
        return handle_404(None)

    if request.method == 'GET':
        return jsonify(character.to_dict()), 200
    try:
        if request.method == 'PATCH':
            data = request.get_json()
            if not data:
                return jsonify({"message": "No data provided"}), 400

            # Validate and update character fields dynamically using Pydantic schema
            # {**character.to_dict(), **data} → Combines current character data (dictionary) with what the user sends
            validated_data = CharacterCreateSchema(**{**character.to_dict(), **data})  # (**merged_dict)

            # Update character fields dynamically
            for key, value in data.items():
                # Loops through data (the user’s input).
                # Updates each field dynamically in the character object.
                setattr(character, key, value)  # no need for if "animal" in data: character.animal = data["animal"]

            db.session.commit()

            return jsonify({
                "message": "Volia! Character updated successfully",
                "character": character.to_dict()
            }), 200

        elif request.method == 'DELETE':
            db.session.delete(character)
            db.session.commit()

            return jsonify({"message": "No problem here: Character deleted successfully."}), 200

    except SQLAlchemyError as db_error:
        db.session.rollback()
        return handle_sqlalchemy_error(db_error)

    except Exception as e:
        db.session.rollback()
        return handle_500(e)

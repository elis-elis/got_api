from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError
from app import db, handle_404, handle_sqlalchemy_error, handle_500, handle_validation_error
from app.models.character_model import Character
from app.schemas.character_schema import CharacterCreateSchema, CharacterUpdateSchema
from app.services.character_db_service import list_characters
from app.utils.filters import get_filter_params
from app.utils.pagination import get_pagination_params
from app.utils.sorting import get_sorting_params


characters_db_bp = Blueprint("characters_db", __name__)


@characters_db_bp.route('/characters/list', methods=['GET'])
@jwt_required(optional=True)  # Authenticated or non-authenticated users can access
def get_character_list():
    """
    Fetch characters with filtering, sorting, and pagination.
    """
    try:
        filters = get_filter_params()

        # Apply sorting
        sort_by, sort_order = get_sorting_params()

        # Apply pagination
        limit, skip = get_pagination_params()

        result = list_characters(filters, sort_by, sort_order, limit, skip)

        if "error" in result:
            return jsonify({"message": result["error"]}), 500

        return jsonify(result), 200

    except ValueError as e:
        return jsonify({"message": str(e)}), 400

    except Exception as e:
        return handle_500(e)


@characters_db_bp.route('/character', methods=['POST'])
@jwt_required()
def create_character_for_db():
    """
    Endpoint to create a new character and save it to the database.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "No data provided"}), 400

        # Validate input
        character_data = CharacterCreateSchema(**data)
        character = Character(**character_data.dict())

        db.session.add(character)
        db.session.commit()

        return jsonify({"message": "Character created successfully", "character": character.to_dict()}), 201

    except ValidationError as ve:
        return handle_validation_error(ve)

    except SQLAlchemyError as db_error:
        db.session.rollback()
        return handle_sqlalchemy_error(db_error)

    except Exception as e:
        db.session.rollback()
        return handle_500(e)


@characters_db_bp.route('/characters/<int:character_id>', methods=['GET', 'PATCH', 'DELETE'])
@jwt_required()
def handle_character_db(character_id):
    """
    Handles fetching (GET), updating (PATCH), and deleting (DELETE) a character by ID.
    - GET: Returns the character details.
    - PATCH: Partially updates character fields, validates the request payload before updating the character.
    - DELETE: Removes the character from the database.
    """
    character = Character.query.get(character_id)
    if not character:
        return handle_404("Character not found")

    if request.method == 'GET':
        return jsonify(character.to_dict()), 200
    try:
        if request.method == 'PATCH':
            data = request.get_json()
            if not data:
                return jsonify({"message": "No data provided"}), 400

            # Validate and update character fields dynamically using Pydantic schema
            # **data means we are passing data as keyword arguments (key=value)
            # .dict(exclude_unset=True → only update provided fields, not overwrite existing values
            validated_data = CharacterUpdateSchema(**data).dict(exclude_unset=True)

            # Update character fields dynamically
            for key, value in validated_data.items():
                # Loops through data (the user’s input).
                # Updates each field dynamically in the character object.
                setattr(character, key, value)  # no need for if "animal" in data: character.animal = data["animal"]

            db.session.commit()

            return jsonify({
                "message": "Voilà! Character updated successfully",
                "character": character.to_dict()
            }), 200

        elif request.method == 'DELETE':
            db.session.delete(character)
            db.session.commit()

            return jsonify({"message": "Character deleted successfully."}), 200

    except ValidationError as ve:
        return handle_validation_error(ve)

    except SQLAlchemyError as db_error:
        db.session.rollback()
        return handle_sqlalchemy_error(db_error)

    except Exception as e:
        db.session.rollback()
        return handle_500(e)

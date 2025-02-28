from sqlalchemy import func
from app.models.character_model import Character
from app.utils.filters import apply_filters
from app.utils.sorting import apply_sorting
from app.utils.db_utils import safe_commit, get_total_count
from sqlalchemy.exc import SQLAlchemyError
from app import handle_sqlalchemy_error, db


def list_characters(filters, sort_by, sort_order, limit, skip):
    """
    Fetch characters from the database with filtering, sorting, and pagination.
    Returns both count (paginated result) & total (unpaginated count).
    """
    try:
        start_query = Character.query

        # Apply filters dynamically to query
        query = apply_filters(start_query, filters)

        # Get total count *before* pagination
        total_count = get_total_count(Character)

        # Apply sorting (unless using random)
        if limit == "random":
            query = query.order_by(func.random()).limit(20)  # Select 20 random rows
            characters = query.all()
        else:
            query = apply_sorting(query, sort_by, sort_order)
            characters = query.offset(skip).limit(limit).all()

        return {
                "characters": [character.to_dict() for character in characters],
                "count": len(characters),  # Number of characters returned after pagination
                "total": total_count  # Total number of characters before pagination
                }

    except SQLAlchemyError as db_error:
        return handle_sqlalchemy_error(db_error)


def create_character_db(character_data):
    """
    Creates a new character in the database.
    """
    try:
        character = Character(**character_data.dict())
        db.session.add(character)
        return safe_commit() or character.to_dict()

    except SQLAlchemyError as db_error:
        return handle_sqlalchemy_error(db_error)


def update_character_db(character, validated_data):
    """
    Updates a character in the database, only modifying fields that changed.
    """
    updated_field = False  # Flag to track if any field is updated, no updates have been made yet

    for key, value in validated_data.items():
        # Checks if the character object has the field named key
        # Checks if the current value of that field is different from the new value
        if hasattr(character, key) and getattr(character, key) != value:
            # If the field exists and needs to be changed, update it with the new value
            setattr(character, key, value)
            updated_field = True  # Mark that an update occurred

    if updated_field:
        return safe_commit() or character.to_dict()

    return character.to_dict()

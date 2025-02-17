from app.models.character_model import Character
from app.utils.filters import apply_filters
from app.utils.sorting import apply_sorting
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
        total_count = db.session.query(Character).count()

        # Apply sorting
        query = apply_sorting(query, sort_by, sort_order)

        # Fetch (only necessary records) characters from the db with pagination, prevents loading too much data at once
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
        db.session.commit()
        return character.to_dict()
    except SQLAlchemyError as db_error:
        db.session.rollback()  # Rollback transaction if commit fails
        return handle_sqlalchemy_error(db_error)


def update_character_db(character, validated_data):
    """
    Updates a character in the database, only modifying fields that changed.
    """
    updated_field = False  # Flag to track if any field is updated

    for key, value in validated_data.items():
        if hasattr(character, key) and getattr(character, key) != value:
            setattr(character, key, value)
            updated_field = True  # Mark that an update occurred

    if updated_field:
        try:
            db.session.commit()
        except SQLAlchemyError as db_error:
            db.session.rollback()
            return handle_sqlalchemy_error(db_error)

    return character.to_dict()

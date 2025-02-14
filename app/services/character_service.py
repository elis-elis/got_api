from models.character import Character
from utils.filter import apply_filters
from utils.sorting import apply_sorting
from utils.pagination import get_pagination_params
from sqlalchemy.exc import SQLAlchemyError
from flask import jsonify

from app import handle_sqlalchemy_error


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
        total_count = query.count()

        # Apply sorting
        query = apply_sorting(query, sort_by, sort_order)

        # Fetch characters from the database with pagination
        characters = query.offset(skip).limit(limit).all()

        return jsonify({
                    "characters": [character.to_dict() for character in characters],
                    "count": len(characters),  # Number of characters returned after pagination
                    "total": total_count  # Total number of characters before pagination
                }), 200

    except SQLAlchemyError as db_error:
        return handle_sqlalchemy_error(db_error)

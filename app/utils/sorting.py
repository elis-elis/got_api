from flask import request
from sqlalchemy import asc, desc
from app.models.character_model import Character, House, Strength


ALLOWED_SORT_FIELDS = {"name", "age", "house", "role", "nickname", "animal", "symbol", "death", "strength"}


def get_sorting_params():
    """Extract and validate sorting parameters from the request arguments."""

    sort_by = request.args.get('sort_by', type=str, default="name")
    sort_order = request.args.get('sort_order', type=str, default="asc").lower()

    if sort_by not in ALLOWED_SORT_FIELDS:
        sort_by = "name"  # Default if invalid field is given

    if sort_order not in ["asc", "desc"]:
        sort_order = "asc"

    return sort_by, sort_order


def apply_sorting(query, sort_by, sort_order):
    """
    Apply sorting dynamically based on the user request.
    """
    if sort_by not in ALLOWED_SORT_FIELDS:
        return query  # If the sorting field is not recognized, return the query unchanged

    # Map of sort fields to their corresponding columns (and optional joins)
    sort_fields = {
        "name": Character.name,
        "age": Character.age,
        "house": House.name,
        "role": Character.role,
        "nickname": Character.nickname,
        "animal": Character.animal,
        "symbol": Character.symbol,
        "death": Character.death,
        "strength": Strength.description
    }
    # Check if the field exists in the map
    if sort_by not in sort_fields:
        return query  # If field is not found, return query unchanged

    # Determine the sorting function
    sort_func = asc if sort_order == "asc" else desc

    # If sorting by 'house' or 'strength', perform the join first
    if sort_by in ["house", "strength"]:
        query = query.join(House if sort_by == "house" else Strength)

    # Apply the sorting
    return query.order_by(sort_func(sort_fields[sort_by]))

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

    sort_func = asc if sort_order == "asc" else desc  # Determine sorting order

    if sort_by == "name":
        query = query.order_by(sort_func(Character.name))

    elif sort_by == "age":
        query = query.order_by(sort_func(Character.age))

    elif sort_by == "house":
        query = query.join(House).order_by(sort_func(House.name))

    elif sort_by == "role":
        query = query.order_by(sort_func(Character.role))

    elif sort_by == "nickname":
        query = query.order_by(sort_func(Character.nickname))

    elif sort_by == "animal":
        query = query.order_by(sort_func(Character.animal))

    elif sort_by == "symbol":
        query = query.order_by(sort_func(Character.symbol))

    elif sort_by == "death":
        query = query.order_by(sort_func(Character.death))

    elif sort_by == "strength":
        query = query.join(Strength).order_by(sort_func(Strength.description))

    return query

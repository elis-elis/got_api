from sqlalchemy import asc, desc
from sqlalchemy.exc import SQLAlchemyError
from flask import request
from app.models import Character, House, Strength
from sqlalchemy.orm import joinedload

ALLOWED_SORT_FIELDS = {"name", "age", "house", "role", "nickname", "animal", "symbol", "death", "strength"}


def get_pagination_params():
    """
    Extract and validate pagination parameters.
    Query Parameters:
    - limit: Number of characters to return (default: 20)
    - skip: Number of characters to skip (default: 0)
    """
    limit = request.args.get('limit', type=int, default=20)
    skip = request.args.get('skip', type=int, default=0)

    if limit <= 0:
        raise ValueError("Limit must be greater than 0.")
    if skip < 0:
        raise ValueError("Skip cannot be negative.")

    return limit, skip


def get_filter_params():
    """
    This function collects filter parameters from the URL query string,
    and then returns a dictionary of filters that have actual values (i.e., not None).
    This ensures that we only work with filters the user explicitly provided.
    Each of these filters will get assigned a value based on the URL query string.
    If the parameter is not present in the URL, Flask will return None for that filter.
    """
    filters = {
        "name": request.args.get('name', type=str),
        "house": request.args.get('house', type=str),
        "house_id": request.args.get('house_id', type=int),
        "strength": request.args.get('strength', type=str),
        "strength_id": request.args.get('strength_id', type=int),
        "animal": request.args.get('animal', type=str),
        "role": request.args.get('role', type=str),
        "age": request.args.get('age', type=int),
        "age_more_than": request.args.get('age_more_than', type=int),
        "age_less_than": request.args.get('age_less_than', type=int)
    }
    # Create a new dictionary that only contains the filters with actual values (i.e., value is not None).
    return {key: value for key, value in filters.items() if value is not None}


def apply_filters(query, filters):
    """
    The function takes in a SQLAlchemy query 'query' and a dictionary of filters 'filters',
    and it applies those filters to the query before executing it.
    It checks if specific filters exist in the 'filters' dictionary.
    If the filter is present, it applies a corresponding filter condition to the query.
    After all filters have been applied, it returns the modified query.
    """
    if "name" in filters:
        # ilike(): case-insensitive matching, f"%{filters['name']}%": allows for partial matches
        query = query.filter(Character.name.ilike(f"%{filters['name']}%"))

    # Filtering by house name using a join to the houses table
    if "house" in filters:
        query = query.join(House).filter(House.name.ilike(f"%{filters['house']}%"))

    # Filtering by strength description using a join to the strengths table
    if "strength" in filters:
        query = query.join(Strength).filter(Strength.description.ilike(f"%{filters['strength']}%"))

    if "role" in filters:
        query = query.filter(Character.role.ilike(f"%{filters['role']}%"))

    if "animal" in filters:
        query = query.filter(Character.animal.ilike(f"%{filters['animal']}%"))

    if "age" in filters:
        query = query.filter(Character.age == filters["age"])

    if "age_more_than" in filters:
        query = query.filter(Character.age >= filters["age_more_than"])

    if "age_less_than" in filters:
        query = query.filter(Character.age <= filters["age_less_than"])

    # Filtering by house ID (exact match) using a join with the House table
    if "house_id" in filters:
        query = query.filter(Character.house_id == filters["house_id"])

    # Filtering by strength ID (exact match) using a join with the Strength table
    if "strength_id" in filters:
        query = query.filter(Character.strength_id == filters["strength_id"])

    return query


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

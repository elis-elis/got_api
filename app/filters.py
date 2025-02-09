from sqlalchemy.exc import SQLAlchemyError
from flask import request
from app.models import Character, House, Strength
from sqlalchemy.orm import joinedload


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
    This function collects filter parameters like name, house, role, etc., from the URL query string,
    and then returns a dictionary of filters that have actual values (i.e., not None).
    This ensures that we only work with filters the user explicitly provided.
    Each of these filters will get assigned a value based on the URL query string.
    If the parameter is not present in the URL, Flask will return None for that filter.
    """
    filters = {
        "name": request.args.get("name", type=str),
        "house": request.args.get("house", type=str),
        "house_id": request.args.get("house_id", type=int),
        "strength": request.args.get("strength", type=str),
        "strength_id": request.args.get("strength_id", type=int),
        "animal": request.args.get("animal", type=str),
        "role": request.args.get("role", type=str),
        "age": request.args.get("age", type=int),
        "age_more_than": request.args.get("age_more_than", type=int),
        "age_less_than": request.args.get("age_less_than", type=int)
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

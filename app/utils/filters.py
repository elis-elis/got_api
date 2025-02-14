from flask import request
from app.models.character_model import Character, House, Strength


def get_filter_params():
    """
    Collects filter parameters from the URL query string, ensuring proper type validation.
    Returns a dictionary of valid filters, ignoring invalid inputs.
    """
    filters = {
        "name": request.args.get('name', type=str),
        "house": request.args.get('house', type=str),
        "strength": request.args.get('strength', type=str),
        "animal": request.args.get('animal', type=str),
        "role": request.args.get('role', type=str)
    }

    # Validate integer filters
    int_fields = ["age", "age_more_than", "age_less_than", "strength_id", "house_id"]

    for field in int_fields:
        value = request.args.get(field)
        if value is not None:
            if not value.isdigit():  # faster check, .isdigit() ensures only numbers are accepted before conversion
                raise ValueError(f"Uff. Invalid value for {field}. Must be a number.")
            filters[field] = int(value)

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

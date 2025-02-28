from flask import request


def get_pagination_params():
    """
    Extract and validate pagination parameters.
    If no limit/skip is defined, return a random subset of 20 characters.

    Query Parameters:
    - limit: Number of characters to return (default: 20)
    - skip: Number of characters to skip (default: 0)
    """
    limit = request.args.get('limit', type=int, default=20)
    skip = request.args.get('skip', type=int, default=0)

    # If limit and skip are completely absent, enable random selection
    if "limit" not in request.args and "skip" not in request.args:
        return "random", None  # Special flag for random selection

    # Default values
    limit = limit if limit is not None else 20
    skip = skip if skip is not None else 0

    if limit <= 0:
        raise ValueError("Limit must be greater than 0.")
    if skip < 0:
        raise ValueError("Skip cannot be negative.")

    return limit, skip

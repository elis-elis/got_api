from flask import request


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

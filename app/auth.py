from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
import jwt
from datetime import timedelta, datetime
import pytz  # to ensure timezone awareness
from app import db
from app.config import Config

# Flask uses Blueprints to organize the application into modules or components.
# Blueprint allows to define routes and logic in separate files, then register them into the main Flask application.
auth_bp = Blueprint('auth', __name__)

# Example list of users (in a real app, it will be stored in a database)
# We use a simple dictionary 'users' where the keys are usernames, and values contain the password (hashed) and role.
# In this case, the passwords are plaintext for simplicity, but should never be stored in plaintext in production.
users = {
    "admin": {"password": "adminpassword", "role": "admin"},
    "user_1": {"password": "userpassword", "role": "user"}
}


@auth_bp.route('login', methods=['POST'])
def login():
    """
    Endpoint to login a user. It expects a JSON body with 'username' and 'password'.
    If the credentials are correct, the server returns a 200 OK response with a success message
    and the generated JWT token.
    If the credentials are invalid, a 401 Unauthorized response is returned with an error message.
    """
    # Retrieves the JSON data sent in the request body.
    # request: Used to access incoming HTTP requests (like the JSON data from the client).
    data = request.get_json()

    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"message": "Username and Password are required."}), 400
    # Extract email and password from the request data
    username = data.get("username")
    password = data.get("password")

    # Check if user exists in predefined list
    user = users.get(username)

    # check_password_hash: A utility function from the werkzeug.security module to check
    # if the provided password matches a hashed password stored in the database.
    if user and check_password_hash(user["password"], password):
        # Generate JWT token if credentials are valid
        token = generate_jwt(username, user["role"])
        return jsonify({"message": "Login successful.", "token": token}), 200
    else:
        return jsonify({"message": "Invalid username or password."}), 401


def generate_jwt(username, role):
    """
    Generate a JWT token that includes the username and role.
    The token is signed with the secret key defined in Config.
    """
    expiration = datetime.now(pytz.utc) + timedelta(hours=1)
    payload = {
        "username": username,
        "role": role,
        "exp": expiration
    }
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")
    return token

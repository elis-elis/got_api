"""
Database Seeding Script

This script populates the PostgreSQL database with initial character data from a JSON file.
It ensures that duplicate entries are not added by checking for existing characters before insertion.

Usage:
    Run this script to seed the database:
        $ python app/seed.py

    The script performs the following:
    - Loads character data from `app/characters.json`
    - Checks if a character already exists in the database (to prevent duplicates)
    - Inserts new characters if they do not already exist
    - Commits the transaction to the database

Modules:
    - `json`: Used for reading character data from a JSON file.
    - `app.db`: Contains the database instance (`db`) initialized in `__init__.py`.
    - `app.create_app`: Initializes a Flask application context to interact with the database.
    - `app.models`: Defines the `Character` model representing the database table.
"""

import json
from app import db, create_app
from app.models import Character


# Initialize the app and database
app = create_app()


def seed_database():
    """
    This function:
    - Loads character data from `app/characters.json`
    - Ensures that duplicate records are not inserted
    - Adds new characters to the database
    - Commits the transaction

    The function runs within an application context to allow database operations.

    Raises:
        FileNotFoundError: If the `characters.json` file is missing.
        JSONDecodeError: If the file is not in valid JSON format.
    """
    with app.app_context():
        try:
            with open("app/characters.json", "r") as file:
                characters = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading character data: {e}")
            return

        # Insert characters into the database if they don't already exist
        for character_data in characters:  # characters is a list of dictionaries (loaded from characters.json)

            # If the query finds a match, existing_character will be an object; otherwise, it will be None
            existing_character = Character.query.filter_by(name=character_data["name"]).first()
            if not existing_character:
                character = Character(**character_data)  # unpacks the dictionary into keyword arguments
                db.session.add(character)

        db.session.commit()
        print("Database successfully added!")


if __name__ == "__main__":
    """
    Runs the seeding script when executed directly.
    This ensures the function is only called when the script is run as a standalone program.
    """
    seed_database()

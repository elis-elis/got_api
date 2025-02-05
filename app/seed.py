import json
from app import db, create_app
from app.models import Character


# Initialize the app and database
app = create_app()


def seed_database():
    with app.app_context():
        with open("app/characters.json", "r") as file:
            characters = json.load(file)

        # Insert characters into the database
        for character_data in characters:  # characters is a list of dictionaries (loaded from characters.json)
            # If the query finds a match, existing_character will be an object; otherwise, it will be None
            existing_character = Character.query.filter_by(name=character_data["name"]).first()
            if not existing_character:
                character = Character(**character_data)  # unpacks the dictionary into keyword arguments
                db.session.add(character)

        db.session.commit()
        print("Database successfully added!")


if __name__ == "__main__":
    seed_database()

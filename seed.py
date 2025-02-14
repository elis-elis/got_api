import os
import json
from app import db, create_app
from app.models.character_model import Character, House, Strength

# Initialize the app and database
app = create_app()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get current directory (data/)
DATA_FILE = os.path.join(BASE_DIR, "data", "characters.json")  # Construct path


def seed_database():
    """
    This function:
    - Loads character data from `data/characters.json`
    - Ensures that duplicate records are not inserted
    - Adds new characters to the database
    - Commits the transaction

    The function runs within an application context to allow database operations.
    """
    with app.app_context():
        try:
            with open(DATA_FILE, "r") as file:
                characters = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading character data: {e}")
            return

        # Fetch existing characters in one query (to prevent repeated DB calls)
        existing_names = {character.name for character in Character.query.with_entities(Character.name).all()}

        new_characters = []

        # Insert houses and strengths if they don't already exist
        for character_data in characters:
            if character_data["name"] in existing_names:
                continue  # Skip duplicates

            # Check if house exists, otherwise create it
            house = House.query.filter_by(name=character_data.get("house")).first()
            if not house and character_data.get("house"):
                house = House(name=character_data["house"])
                db.session.add(house)
                db.session.flush()  # Get the ID before committing

            # Check if strength exists, otherwise create it
            strength = Strength.query.filter_by(description=character_data.get("strength")).first()
            if not strength and character_data.get("strength"):
                strength = Strength(description=character_data["strength"])
                db.session.add(strength)
                db.session.flush()

                # Append new character to the list
                new_characters.append(
                    Character(
                        name=character_data["name"],
                        house=house,
                        animal=character_data.get("animal"),
                        symbol=character_data.get("symbol"),
                        nickname=character_data.get("nickname"),
                        role=character_data["role"],
                        age=character_data.get("age"),
                        death=character_data.get("death"),
                        strength=strength
                    )
                )
            # Bulk insert all new characters
            db.session.bulk_save_objects(new_characters)
        try:
            db.session.commit()
            print("Lovely! Database successfully added!")

        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading character data: {e}")

        except Exception as e:
            db.session.rollback()  # Roll back any partial inserts
            print(f"Database error: {e}")


if __name__ == "__main__":
    """
    Runs the seeding script when executed directly.
    This ensures the function is only called when the script is run as a standalone program.
    """
    seed_database()

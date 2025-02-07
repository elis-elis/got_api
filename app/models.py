"""
Separate houses and strengths into their own tables and reference them using foreign keys in the characters table.
Separating them into distinct tables removes redundancy, enforces uniformity.
"""

from app import db


class Character(db.Model):
    __tablename__ = "characters"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    house_id = db.Column(db.Integer, db.ForeignKey("houses.id"), nullable=True)
    animal = db.Column(db.String(50), nullable=True)
    symbol = db.Column(db.String(50), nullable=True)
    nickname = db.Column(db.String(50), nullable=True)
    role = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    death = db.Column(db.Integer, nullable=True)
    strength_id = db.Column(db.Integer, db.ForeignKey("strengths.id"), nullable=True)

    house = db.relationship("House", back_populates="characters")
    strength =db.relationship("Strength", back_populates="characters")

    def __repr__(self):
        # method helps in debugging by providing a string representation
        return f"<Character {self.name}>"


class House(db.Model):
    __tablename__ = "houses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    characters = db.relationship("Character", back_populates="house")

    def __repr__(self):
        return f"<House {self.name}>"


class Strength(db.Model):
    __tablename__ = "strengths"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50), nullable=False, unique=True)

    characters = db.relationship("Character", back_populates="strength")

    def __repr__(self):
        return f"<Strength {self.description}>"

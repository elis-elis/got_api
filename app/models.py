from app import db


class Character(db.Model):
    __tablename__ = "characters"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    house = db.Column(db.String(50), nullable=True)
    animal = db.Column(db.String(50), nullable=True)
    symbol = db.Column(db.String(50), nullable=True)
    nickname = db.Column(db.String(50), nullable=True)
    role = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    death = db.Column(db.Integer, nullable=True)
    strength = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        # method helps in debugging by providing a string representation
        return f"<Character {self.name} of House {self.house}>"

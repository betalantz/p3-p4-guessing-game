from app import app
from db import db
from models import Game, Round, User
from sqlalchemy import delete


def seed():
    """Seed tables"""

    print("Clearing tables")
    db.session.execute(delete(Round))
    db.session.execute(delete(Game))
    db.session.execute(delete(User))

    print("Seeding tables")
    user1 = User(name="user1", password="flatiron")
    user2 = User(name="user2", password="flatiron")
    db.session.add_all([user1, user2])
    db.session.commit()
    game1 = Game(user=user1, difficulty="easy", range_min=1, range_max=10)
    game1.new_round()
    game2 = Game(user=user1, difficulty="hard", range_min=1, range_max=100)
    game2.new_round()
    db.session.add_all([game1, game2])
    db.session.commit()
    print("Seeding tables finished")


if __name__ == "__main__":
    with app.app_context():
        seed()

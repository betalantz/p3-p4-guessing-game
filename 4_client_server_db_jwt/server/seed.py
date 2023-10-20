from app import app
from db import db
from models import Game, Round, User
from sqlalchemy import delete


def seed():
    """Seed tables"""
    db.session.execute(delete(Round))
    db.session.execute(delete(Game))
    db.session.execute(delete(User))
    user1 = User(name="user1", password="flatiron")
    user2 = User(name="user2", password="flatiron")
    db.session.add_all([user1, user2])
    db.session.commit()
    game1 = Game(user=user1, difficulty="easy", range_min=1, range_max=10)
    game2 = Game(user=user1, difficulty="hard", range_min=1, range_max=100)
    game3 = Game(user=user2, difficulty="easy", range_min=1, range_max=50)
    db.session.add_all([game1, game2, game3])
    db.session.commit()
    db.session.add(game1.new_round())
    db.session.add(game2.new_round())
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        seed()

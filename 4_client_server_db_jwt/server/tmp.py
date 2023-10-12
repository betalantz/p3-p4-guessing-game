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
    db.session.add(user1)
    db.session.commit()
    game1 = Game(user=user1, difficulty="easy", range_min=1, range_max=10)
    game2 = Game(user=user1, difficulty="hard", range_min=1, range_max=100)
    db.session.add_all([game1, game2])
    db.session.commit()
    db.session.add(
        Round(game=game1, range_min=game1.range_min, range_max=game1.range_max)
    )
    db.session.add(Round(game=game1, range_min=5, range_max=8))
    db.session.add(
        Round(game=game2, range_min=game2.range_min, range_max=game2.range_max)
    )
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        seed()

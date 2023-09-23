from sqlalchemy import delete

from app import app
from models import db, Game, Round


def seed():
    """Seed tables"""
    db.session.execute(delete(Round))
    db.session.execute(delete(Game))
    game1 = Game(difficulty="easy", min_value = 1, max_value = 10)
    game2 = Game(difficulty="hard", min_value = 1, max_value = 100)
    db.session.add_all([game1, game2])
    db.session.commit()
    db.session.add(Round(game=game1, min_value=game1.min_value, max_value=game1.max_value))
    db.session.add(Round(game=game1, min_value=5, max_value=8))
    db.session.add(Round(game=game2, min_value=game2.min_value, max_value=game2.max_value))
    db.session.commit()
    

if __name__ == '__main__':
    with app.app_context():
        seed()

from app import app
from models import Game, Round, db
from sqlalchemy import delete


def seed():
    """Seed tables"""

    print("Clearing tables")
    db.session.execute(delete(Round))
    db.session.execute(delete(Game))

    print("Seeding tables")
    game1 = Game(difficulty="easy", range_min=1, range_max=10)
    game1.new_round()
    game2 = Game(difficulty="hard", range_min=1, range_max=100)
    game2.new_round()
    db.session.add_all([game1, game2])
    db.session.commit()
    print("Seeding tables finished")


if __name__ == "__main__":
    with app.app_context():
        seed()

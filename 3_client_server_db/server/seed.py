from models import Game, Round


def seed():
    from app import app

    with app.app_context():
        print("Clearing memory")
        Round.all.clear()
        Game.all.clear()

        print("Seeding memory")
        game1 = Game(difficulty="easy", range_min=1, range_max=10)
        game1.new_round()
        game2 = Game(difficulty="hard", range_min=1, range_max=100)
        game2.new_round()
        print("Seeding memory finished")


if __name__ == "__main__":
    from app import app

    with app.app_context():
        seed()

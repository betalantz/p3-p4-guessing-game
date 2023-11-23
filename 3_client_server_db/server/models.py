import logging
from enum import StrEnum, auto
from random import randint

logger = logging.getLogger(__name__)

# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import MetaData

# metadata = MetaData(
#     naming_convention={
#         "pk": "pk_%(table_name)s",
#         "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
#         "ix": "ix_%(table_name)s_%(column_0_name)s",
#         "uq": "uq_%(table_name)s_%(column_0_name)s",
#         "ck": "ck_%(table_name)s_%(constraint_name)s",
#     }
# )

# db = SQLAlchemy(metadata=metadata)


# remove enums for v3 and reintroduce for v4?
class GuessStatus(StrEnum):
    CORRECT = auto()
    HIGH = auto()
    LOW = auto()
    INVALID = auto()


class DifficultyLevel(StrEnum):
    EASY = auto()
    HARD = auto()


class Round:
    all = []

    def __init__(self, game, range_min, range_max, number):
        self.id = len(type(self).all) + 1
        self.game = game
        self.range_min = range_min
        self.range_max = range_max
        self.number = number
        self.guess = None
        self.status = None
        Round.all.append(self)

    def update(self, guess):
        """Update the current round based on the guess"""
        logger.debug(f"Updating round {self.id} with guess {guess}")
        if self.status:
            raise RuntimeError("Round status has already been set.")
        self.guess = guess
        if guess == self.game.secret_number:
            self.status = GuessStatus.CORRECT
        else:
            if guess < self.range_min or guess > self.range_max:
                self.status = GuessStatus.INVALID
            elif guess > self.game.secret_number:
                self.status = GuessStatus.HIGH
            else:
                self.status = GuessStatus.LOW


# class Round(db.Model):
#     """Round model"""

#     __tablename__ = "rounds"
#     id = db.Column(db.Integer, primary_key=True)
#     range_min = db.Column(db.Integer, nullable=False)
#     range_max = db.Column(db.Integer, nullable=False)
#     number = db.Column(db.Integer, nullable=False)
#     guess = db.Column(db.Integer)
#     status = db.Column(db.String)

#     game_id = db.Column(db.Integer, db.ForeignKey("games.id"), nullable=False)
#     game = db.relationship("Game", back_populates="rounds")

#     __table_args__ = (
#         db.CheckConstraint("range_min <= range_max", name="min_max_range"),
#     )

#     def update(self, guess):
#         """Update the current round based on the guess"""
#         if self.status:
#             raise RuntimeError("Round status has already been set.")
#         self.guess = guess
#         if guess == self.game.secret_number:
#             self.status = GuessStatus.CORRECT
#         else:
#             if guess < self.range_min or guess > self.range_max:
#                 self.status = GuessStatus.INVALID
#             elif guess > self.game.secret_number:
#                 self.status = GuessStatus.HIGH
#             else:
#                 self.status = GuessStatus.LOW


def create_secret_number(range_min, range_max):
    return randint(range_min, range_max)


class Game:
    all = []

    def __init__(self, difficulty, range_min, range_max):
        self.id = len(type(self).all) + 1
        self.difficulty = difficulty
        self.range_min = range_min
        self.range_max = range_max
        self.secret_number = create_secret_number(range_min, range_max)
        self.is_over = False
        Game.all.append(self)
        logger.debug(f"Game object created and added to Game.all: {self.__dict__}")

    @property
    def rounds(self):
        return [round for round in Round.all if round.game == self]

    @property
    def current_round(self):
        return (
            max(self.rounds, key=lambda round: round.number)
            if len(self.rounds)
            else None
        )

    @property
    def number_of_rounds(self):
        return len(self.rounds)

    def new_round(self):
        if self.is_over:
            raise RuntimeError(f"Error creating new round. Game {self.id} is over.")
        if self.rounds:
            # create next round based on current round
            round = self.current_round
            if round.status is None:
                raise RuntimeError(
                    f"Current round {round.id} status must be set prior to creating a new round."
                )
            next_min = round.range_min
            next_max = round.range_max
            if self.difficulty == DifficultyLevel.EASY:
                if round.status == GuessStatus.HIGH:
                    next_max = round.guess - 1
            return Round(
                game=self,
                range_min=next_min,
                range_max=next_max,
                number=round.number + 1,
            )
        else:
            # create 1st round
            return Round(
                game=self, range_min=self.range_min, range_max=self.range_max, number=1
            )

    def update(self, guess, round_id):
        """Update the current game based on the guess"""
        if self.is_over:
            raise RuntimeError(f"Game {self.id} is over.")
        """Only allow the current round to be updated"""
        if self.current_round.id == round_id:
            logger.debug(f"Updating game {self.id} with guess {guess}")
            if self.rounds:
                round = self.current_round
                round.update(guess)
                if round.status == GuessStatus.CORRECT:
                    self.is_over = True

            else:
                raise RuntimeError(
                    f"Error updating game {self.id}. Game does not contain a round to update."
                )
        else:
            raise RuntimeError(
                f"Error updating game {self.id}. Round {round_id} is not current round."
            )


# class Game(db.Model):
#     """Game model"""

#     __tablename__ = "games"
#     id = db.Column(db.Integer, primary_key=True)
#     difficulty = db.Column(db.String, nullable=False)
#     range_min = db.Column(db.Integer, nullable=False)
#     range_max = db.Column(db.Integer, nullable=False)
#     secret_number = db.Column(db.Integer, default=create_secret_number)
#     is_over = db.Column(db.Boolean, default=False)

#     rounds = db.relationship(
#         "Round", back_populates="game", cascade="all, delete-orphan"
#     )

#     __table_args__ = (
#         db.CheckConstraint("range_min <= range_max", name="min_max_range"),
#     )

#     def current_round(self):
#         return max(self.rounds, key=lambda round: round.number) if self.rounds else None

#     def new_round(self):
#         if self.is_over:
#             raise RuntimeError(f"Error creating new round. Game {self.id} is over.")
#         if self.rounds:
#             # create next round based on current round
#             round = self.current_round()
#             if round.status is None:
#                 raise RuntimeError(
#                     f"Current round {round.id} status must be set prior to creating a new round."
#                 )
#             next_min = round.range_min
#             next_max = round.range_max
#             if self.difficulty == DifficultyLevel.EASY:
#                 if round.status == GuessStatus.HIGH:
#                     next_max = round.guess - 1  # adjust range_max for next round
#                 elif round.status == GuessStatus.LOW:
#                     next_min = round.guess + 1  # adjust range_min for next round
#             return Round(
#                 game=self,
#                 range_min=next_min,
#                 range_max=next_max,
#                 number=round.number + 1,
#             )
#         else:
#             # create 1st round
#             return Round(
#                 game=self, range_min=self.range_min, range_max=self.range_max, number=1
#             )

#     def update(self, guess, round_id):
#         """Update the current game based on the guess"""
#         if self.is_over:
#             raise RuntimeError(f"Game {self.id} is over.")
#         """Only allow the current round to be updated"""
#         if self.current_round().id == round_id:
#             if self.rounds:
#                 round = self.current_round()
#                 round.update(guess)
#                 if round.status == GuessStatus.CORRECT:
#                     self.is_over = True

#             else:
#                 raise RuntimeError(
#                     f"Error updating game {self.id}. Game does not contain a round to update."
#                 )
#         else:
#             raise RuntimeError(
#                 f"Error updating game {self.id}. Round {round_id} is not current round."
#             )

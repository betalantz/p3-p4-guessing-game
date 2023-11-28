from enum import StrEnum, auto
from random import randint

# remove enums for v3 and reintroduce for v4?
# class GuessStatus(StrEnum):
#     CORRECT = auto()
#     HIGH = auto()
#     LOW = auto()
#     INVALID = auto()

GUESS_STATUS = {
    "CORRECT": "correct",
    "HIGH": "high",
    "LOW": "low",
    "INVALID": "invalid",
}

DIFFICULTY_LEVEL = {
    "EASY": "easy",
    "HARD": "hard",
}


# class DifficultyLevel(StrEnum):
#     EASY = auto()
#     HARD = auto()


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
        if self.status:
            raise RuntimeError("Round status has already been set.")
        self.guess = guess
        if guess == self.game.secret_number:
            self.status = GUESS_STATUS["CORRECT"]
        else:
            if guess < self.range_min or guess > self.range_max:
                self.status = GUESS_STATUS["INVALID"]
            elif guess > self.game.secret_number:
                self.status = GUESS_STATUS["HIGH"]
            else:
                self.status = GUESS_STATUS["LOW"]


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
            if self.difficulty == DIFFICULTY_LEVEL["EASY"]:
                if round.status == GUESS_STATUS["HIGH"]:
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
            if self.rounds:
                round = self.current_round
                round.update(guess)
                if round.status == GUESS_STATUS["CORRECT"]:
                    self.is_over = True

            else:
                raise RuntimeError(
                    f"Error updating game {self.id}. Game does not contain a round to update."
                )
        else:
            raise RuntimeError(
                f"Error updating game {self.id}. Round {round_id} is not current round."
            )

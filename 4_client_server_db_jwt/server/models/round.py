from db import db
from models import DifficultyLevel, GuessStatus


class Round(db.Model):
    """Round model"""

    __tablename__ = "rounds"
    id = db.Column(db.Integer, primary_key=True)
    range_min = db.Column(db.Integer, nullable=False)
    range_max = db.Column(db.Integer, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    guess = db.Column(db.Integer)
    status = db.Column(db.String)

    game_id = db.Column(db.Integer, db.ForeignKey("games.id"), nullable=False)
    game = db.relationship("Game", back_populates="rounds")

    __table_args__ = (
        db.CheckConstraint("range_min <= range_max", name="min_max_range"),
    )

    def update(self, guess):
        """Update the current round based on the guess"""
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

from random import randint
from db import db
from models import  Round, GuessStatus, DifficultyLevel


def create_secret_number(context):
    return randint(context.get_current_parameters()["range_min"], context.get_current_parameters()["range_max"]);

class Game(db.Model):
    """Game model"""
    __tablename__ = "games"
    id = db.Column(db.Integer, primary_key=True)
    
    difficulty = db.Column(db.String, nullable=False)
    range_min = db.Column(db.Integer, nullable=False)
    range_max = db.Column(db.Integer, nullable=False)
    secret_number = db.Column(db.Integer, default=create_secret_number)
    is_over = db.Column(db.Boolean, default=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="games")
 
    rounds = db.relationship(
        "Round", back_populates="game", cascade="all, delete-orphan")

    __table_args__ = (
        db.CheckConstraint("range_min <= range_max", name="min_max_range"),
    )
            
    def play_round(self, guess):
        """Update the current round based on the guess"""
        if self.is_over: 
            raise Exception("Game is over.")
        current_round = max(self.rounds, key=lambda round: round.id)
        current_round.guess = guess
        if guess == self.secret_number:
            current_round.status = GuessStatus.CORRECT
            self.is_over = True
        else:
            #assign status to current round and create the next round of play
            next_min = current_round.range_min
            next_max = current_round.range_max
            if guess < current_round.range_min or guess > current_round.range_max:
                current_round.status = GuessStatus.INVALID
            elif guess > self.secret_number:
                current_round.status = GuessStatus.HIGH
                if self.difficulty == DifficultyLevel.EASY:
                    next_max = guess - 1  #adjust range_max for next round   
            else:
                current_round.status = GuessStatus.LOW
                if self.difficulty == DifficultyLevel.EASY:
                    next_min= guess + 1  #adjust range_min for next round      

            return Round(game = self, range_min = next_min, range_max = next_max) #create next round
        
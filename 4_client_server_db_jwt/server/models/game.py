from random import randint
from db import db
from models import Round, GuessStatus, DifficultyLevel


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
    
    def current_round(self):
        return max(self.rounds, key=lambda round: round.number) if self.rounds else None
    
    def new_round(self):
        if self.is_over:
            raise RuntimeError(f"Error creating new round. Game {self.id} is over.")
        if self.rounds:
            #create next round based on current round
            round = self.current_round()
            if round.status is None: 
                raise RuntimeError(f"Current round {round.id} status must be set prior to creating a new round.")
            next_min = round.range_min
            next_max = round.range_max
            if self.difficulty == DifficultyLevel.EASY:
                if round.status == GuessStatus.HIGH:
                    next_max = round.guess - 1  #adjust range_max for next round   
                elif round.status == GuessStatus.LOW:
                    next_min= round.guess + 1  #adjust range_min for next round  
            return Round(game = self, range_min = next_min, range_max = next_max, number = round.number + 1)
        else:
            #create 1st round
            return Round(game = self, range_min = self.range_min, range_max = self.range_max, number =  1)            

    def update(self, guess):
            """Update the current round based on the guess"""
            if self.is_over: 
                raise RuntimeError(f"Error updating current round. Game {self.id} is over.")
            if self.rounds:
                round = self.current_round()
                round.update(guess)
                if round.status == GuessStatus.CORRECT:
                    self.is_over = True
            else:
                raise RuntimeError(f"Error updating game {self.id}. Game does not contain a round to update.")
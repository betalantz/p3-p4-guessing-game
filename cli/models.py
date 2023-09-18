from random import randint
from enum import Enum
import uuid

class Status(Enum):
    CORRECT = "correct"
    HIGH = "too high"
    LOW= "too low"
    INVALID = "outside of range"
    
class Round():
    
    all = []
    
    def __init__(self, game, min_value, max_value):
        self.game = game
        self.min_value = min_value
        self.max_value = max_value
        self.guess = None 
        self.status = None 
        type(self).all.append(self) 

class Game():
    
    all = []
    
    def __init__(self , min_value, max_value):
        self.id = str(uuid.uuid4())
        self.secret_number = randint(min_value, max_value)
        self.is_over = False
        type(self).all.append(self)
        Round(self, min_value, max_value)  #setup first round of play
        
    def get_rounds(self) : 
        """Get list of rounds for this game"""
        return [round for round in Round.all if round.game is self]
 
    def get_current_round(self):
        """Get last round in list"""
        return self.get_rounds()[-1]  
            
    def play_round(self, guess):
        """Update the current round based on the guess"""
        if self.is_over: 
            raise Exception("Game is over.")
        current_round = self.get_current_round()
        current_round.guess = guess
        if guess == self.secret_number:
            current_round.status = Status.CORRECT
            self.is_over = True
        elif guess < current_round.min_value or guess > current_round.max_value:
            current_round.status = Status.INVALID
            Round(self, current_round.min_value, current_round.max_value)  #same range for next round
        elif guess > self.secret_number:
            current_round.status = Status.HIGH
            Round(self, current_round.min_value, guess - 1) #adjust max_value for next round
        else:
            current_round.status = Status.LOW
            Round(self, guess + 1, current_round.max_value) #adjust min_value for next round
            
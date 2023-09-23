from random import randint
from enum import  StrEnum, auto
import uuid

class GuessStatus(StrEnum):
    CORRECT = auto() 
    HIGH = auto()    
    LOW= auto()      
    INVALID = auto() 
    
class DifficultyLevel(StrEnum):
    EASY = auto()   
    HARD= auto()   
  
class Round():
    
    all = [] #list
    
    def __init__(self, game, min_value, max_value):
        self.game = game
        self.min_value = min_value
        self.max_value = max_value
        self.guess = None 
        self.status = None 
        type(self).all.append(self) 

class Game():
    
    all = {}  #dictionary with id as key
    
    def __init__(self , level, min_value, max_value):
        self.id = str(uuid.uuid4())
        self.level = level
        self.min_value = min_value
        self.max_value = max_value
        self.secret_number = randint(min_value, max_value)
        self.is_over = False
        type(self).all[self.id] = self
        Round(self, min_value, max_value)  #setup first round of play
        
    def get_rounds(self) : 
        """Get list of rounds for this game"""
        return [round for round in Round.all if round.game is self]
            
    def play_round(self, guess):
        """Update the current round based on the guess"""
        if self.is_over: 
            raise Exception("Game is over.")
        current_round = self.get_rounds()[-1]  #last round in list
        current_round.guess = guess
        if guess == self.secret_number:
            current_round.status = GuessStatus.CORRECT
            self.is_over = True
        else:
            #assign status to current round and create the next round of play
            next_min = current_round.min_value
            next_max = current_round.max_value
            if guess < current_round.min_value or guess > current_round.max_value:
                current_round.status = GuessStatus.INVALID
            elif guess > self.secret_number:
                current_round.status = GuessStatus.HIGH
                if self.level is DifficultyLevel.EASY:
                    next_max = guess - 1  #adjust max_value for next round   
            else:
                current_round.status = GuessStatus.LOW
                if self.level is DifficultyLevel.EASY:
                    next_min= guess + 1  #adjust min_value for next round      

            Round(self, next_min, next_max) #create next round
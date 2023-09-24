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
    
    def __init__(self, game, range_min, range_max):
        self.game = game
        self.range_min = range_min
        self.range_max = range_max
        self.guess = None 
        self.status = None 
        type(self).all.append(self) 

class Game():
    
    all = {}  #dictionary with id as key
    
    def __init__(self , difficulty, range_min, range_max):
        self.id = str(uuid.uuid4())
        self.difficulty = difficulty
        self.range_min = range_min
        self.range_max = range_max
        self.secret_number = randint(range_min, range_max)
        self.is_over = False
        type(self).all[self.id] = self
        Round(self, range_min, range_max)  #setup first round of play
        
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

            Round(self, next_min, next_max) #create next round
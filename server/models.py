from random import randint
import uuid
from schemas import *

class Round():
    
    def __init__(self, minValue, maxValue, guess, status = None):
        self.minValue = minValue
        self.maxValue = maxValue
        self.guess = guess 
        self.status = status 

class Game():
    
    all = {}
    
    def __init__(self , minValue, maxValue):
        self.id = len(self.all) + 1      # str(uuid.uuid4())
        self.minValue = minValue
        self.maxValue = maxValue
        self.secretNumber = randint(self.minValue, self.maxValue)
        self.isOver = False
        self.rounds = []
        type(self).all[self.id] = self  
        
    def playRound(self, guess) :
        if not self.gameOver: 
            round = Round(self.minValue, self.maxValue, guess)
            if guess == self.secretNumber:
                round.status = "correct"
                self.isOver = True
            elif round.guess < self.minValue or round.guess > self.maxValue:
                round.status = "invalid"
            elif round.guess > self.secretNumber:
                round.status = "too high"
                self.maxValue = round.guess - 1 
            else:
                round.status = "too low"
                self.minValue = round.guess + 1
            self.rounds.append( round )
        

    
    
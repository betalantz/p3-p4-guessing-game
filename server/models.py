from random import randint
import uuid

class Round():
    
    all = {}
    
    def __init__(self, game_id, minValue, maxValue, guess, status = None):
        self.id = len(self.all) + 1      # str(uuid.uuid4())
        self.game_id = game_id
        self.minValue = minValue
        self.maxValue = maxValue
        self.guess = guess 
        self.status = status 
        type(self).all[self.id] = self 

class Game():
    
    all = {}
    
    def __init__(self , minValue, maxValue):
        self.id = len(self.all) + 1      # str(uuid.uuid4())
        self.minValue = minValue
        self.maxValue = maxValue
        self.secretNumber = randint(self.minValue, self.maxValue)
        self.isOver = False
        type(self).all[self.id] = self 
        
    def rounds(self) : 
        """Get list of rounds for this game"""
        return [round for round in Round.all.values() if round.game_id == self.id]
 
    def playRound(self, guess) :
        if not self.isOver: 
            round = Round(self.id, self.minValue, self.maxValue, guess)
            if guess == self.secretNumber:
                round.status = "correct"
                self.isOver = True
            elif guess < self.minValue or guess > self.maxValue:
                round.status = "invalid"
            elif guess > self.secretNumber:
                round.status = "too high"
                self.maxValue = round.guess - 1 #adjust for next round
            else:
                round.status = "too low"
                self.minValue = round.guess + 1 #adjust for next round
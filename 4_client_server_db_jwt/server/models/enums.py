from enum import  StrEnum, auto

class DifficultyLevel(StrEnum):
    EASY = auto()   
    HARD= auto()   
    
class GuessStatus(StrEnum):
    CORRECT = auto() 
    HIGH = auto()    
    LOW= auto()      
    INVALID = auto() 
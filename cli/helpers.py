from models import Game
from schemas import GameSchema
from marshmallow import ValidationError
from pprint import pprint
from random import randint
from math import log, ceil

def exit_program():
    print("Goodbye!")
    exit()

def list_games():
    schema = GameSchema()
    [pprint(schema.dump(game)) for game in Game.all]
            
def new_game():
    min_value = input("Enter the minimum value: ")
    max_value = input("Enter the maximum value: ")
    try : 
        schema = GameSchema()
        game = schema.load({"min_value" : min_value, "max_value" : max_value})
        max_rounds = ceil(log((game.max_value - game.min_value + 1), 2))
        #pprint(schema.dump(game))
        while not game.is_over:
            current_round = game.get_current_round()
            #should be able to guess by picking midpoint of range each round.
            if len(game.get_rounds()) > max_rounds:
                rand = randint(3, 5)  #3,4,5
                print(f"HINT: What is {game.secret_number - 2 ** rand} + 2**{rand}?")  #practice powers of 2
            response = input(f"Guess an integer between {current_round.min_value} and {current_round.max_value}: ")
            try :
                guess = int(response)
                game.play_round(guess)
                print(f"{guess} is {current_round.status.value}.")
            except Exception:
                print(f"{response} is not an integer.")
    except ValidationError as err:
        print(err.messages)
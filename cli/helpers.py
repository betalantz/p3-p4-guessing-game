from models import Game
from schemas import GameSchema
from marshmallow import ValidationError
from pprint import pprint

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
        #pprint(schema.dump(game))
        while not game.is_over:
            current_round = game.get_current_round()
            response = input(f"Guess an integer between {current_round.min_value} and {current_round.max_value}: ")
            try :
                guess = int(response)
                game.play_round(guess)
                print(f"{guess} is {current_round.status.value}.")
            except Exception:
                print(f"{response} is not an integer.")
    except ValidationError as err:
        print(err.messages)
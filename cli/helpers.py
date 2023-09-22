from models import Game, Level, Status
from schemas import GameSchema
from marshmallow import ValidationError
from pprint import pprint

def exit_program():
    print("Goodbye!")
    exit()

def list_games():
    schema = GameSchema()
    [pprint(schema.dump(game)) for game in Game.all]
    
def response_message(round):
    match round.status:
        case Status.CORRECT:
            return f"{round.guess} is correct!"
        case Status.LOW:
            return f"{round.guess} is too low."
        case Status.HIGH:
            return f"{round.guess} is too high."
        case Status.INVALID:
            return f"{round.guess} is outside the range {round.min_value}..{round.max_value}."
            
def new_game():
    try :
        str = input("Enter the difficulty level (EASY/HARD): ")
        level = Level[str]
        min_value = input("Enter the minimum value: ")
        max_value = input("Enter the maximum value: ")
        schema = GameSchema()
        game = schema.load({"level" : level, "min_value" : min_value, "max_value" : max_value})
        #pprint(schema.dump(game))
        while not game.is_over:
            current_round = game.get_rounds()[-1]  #last round in list
            response = input(f"Guess an integer between {current_round.min_value} and {current_round.max_value} (inclusive): ")
            try :
                guess = int(response)
                game.play_round(guess)
                print(response_message(current_round))
            except Exception:
                print(f"{response} is not an integer.")
    except KeyError as err:
        print(f"{err} is not a valid level")
    except ValidationError as err:
        print(err.messages)
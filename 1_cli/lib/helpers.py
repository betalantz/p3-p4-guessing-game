from models import Game, Round, GuessStatus
from schemas import GameSchema, RoundSchema
from marshmallow import ValidationError
from pprint import pprint

def exit_program():
    print("Goodbye!")
    exit()

def response_message(round):
    match round.status:
        case GuessStatus.CORRECT:
            return f"{round.guess} is correct!"
        case GuessStatus.LOW:
            return f"{round.guess} is too low."
        case GuessStatus.HIGH:
            return f"{round.guess} is too high."
        case GuessStatus.INVALID:
            return f"{round.guess} is outside the range {round.range_min}..{round.range_max}."
            
def new_game():
    try :
        difficulty = input("Enter the level of difficulty (easy or hard): ")
        range_min = input("Enter the minimum value: ")
        range_max = input("Enter the maximum value: ")
        schema = GameSchema()
        game = schema.load({"difficulty" : difficulty, "range_min" : range_min, "range_max" : range_max})
        #pprint(schema.dump(game))
        while not game.is_over:
            current_round = game.get_rounds()[-1]  #last round in list
            response = input(f"Guess an integer between {current_round.range_min} and {current_round.range_max} (inclusive): ")
            try :
                guess = int(response)
                game.play_round(guess)
                print(response_message(current_round))
            except Exception:
                print(f"{response} is not an integer.")
    except ValidationError as err:
        print(err.messages)
           
def list_games():
    schema = GameSchema()
    [pprint(schema.dump(game)) for game in Game.all.values()]
    
def list_game_by_id():
    id = input(f"Enter game id: ")
    game = Game.all.get(id)
    pprint(GameSchema().dump(game)) if game else print(f"Game {id} not found.")
    
def list_rounds():
    schema = RoundSchema()
    [pprint(schema.dump(round)) for round in Round.all]
    
def list_rounds_by_game_id():
    id = input("Enter game id: ")
    game = Game.all.get(id)
    if game:
        schema = RoundSchema()
        [pprint(schema.dump(round)) for round in Round.all if round.game.id == id]
    else:
        print(f"Game {id} not found.")
  
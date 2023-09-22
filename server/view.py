from flask.views import MethodView
from flask_smorest import Blueprint, abort

from models import Game, Round
from schemas import GameSchema, GameUpdateSchema, RoundSchema

blp = Blueprint("Guessing Game API", __name__)

@blp.route("/games")
class Games(MethodView):
    
    @blp.response(200, GameSchema(many=True))
    def get(self):
        """List games"""
        return Game.all.values()
    
    @blp.arguments(GameSchema)
    @blp.response(201, GameSchema)
    def post(self, fields):
        """Create a new game"""
        return Game(**fields)

@blp.route("/games/<string:game_id>")
class GamesById(MethodView):
    
    @blp.response(200, GameSchema)
    def get(self, game_id):
        """Get game by id"""
        game = Game.all.get(game_id)
        if game is None:
            abort(404, message=f"Game {game_id} not found.")
        return game
    
    
    @blp.arguments(GameUpdateSchema)
    @blp.response(200, GameSchema)
    def patch(self, fields, game_id):
        """Update game by id.  Update current round based on the guess."""
        game = Game.all.get(game_id)
        if game is None:
            abort(404, message=f"Game {game_id} not found.")
        if game.is_over:
            abort(409, message=f"Game {game_id} is over, no more guessing.")
        game.play_round(fields["guess"])
        return game
    
    @blp.response(204)
    def delete(self, game_id):
        """Delete game and associated rounds by id"""
        game = Game.all.get(game_id)
        if game is None:
            abort(404, message=f"Game {game_id} not found.")
        # Exclude all rounds associated with this game
        Round.all = [round for round in Round.all if round.game is not game]
        # Exclude the game from the dictionary
        del Game.all[game_id]
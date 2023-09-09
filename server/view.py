from flask.views import MethodView
from flask_smorest import Blueprint, abort

from models import Game
from schemas import GameSchema, GameUpdateSchema

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

@blp.route("/games/<int:game_id>")
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
        """Update game by id.  Add a new round of play based on the guess."""
        game = Game.all.get(game_id)
        if game is None:
            abort(404, message=f"Game {game_id} not found.")
        if game.isOver:
            abort(409, message=f"Game {game_id} is over, no more guessing.")
        game.playRound(fields["guess"])
        return game
    
    @blp.response(204)
    def delete(self, game_id):
        """Delete game by id"""
        try:
            del Game.all[game_id]
        except KeyError:
            abort(404, message=f"Game {game_id} not found.")

        

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
        return GameSchema().dump(Game.all(), many=True)

    @blp.arguments(GameSchema)
    @blp.response(201, GameSchema)
    def post(self, fields):
        """Create a new game and 1st round of play"""
        try:
            game = Game(**fields)
            round = game.new_round()
        except Exception as err:
            abort(400, game=err.__class__.__name__, errors=[str(x) for x in err.args])
        return GameSchema().dump(game), 201


@blp.route("/games/<int:game_id>")
class GamesById(MethodView):
    @blp.arguments(GameUpdateSchema)
    @blp.response(200, GameSchema)
    def patch(self, fields, game_id):
        """Update game by id.  Update current round based on the guess."""
        game = [game for game in Game.all() if game.id == game_id].first()
        try:
            game.update(**fields)
            if not game.is_over:
                next_round = game.new_round()
            return GameSchema().dump(game)
        except Exception as err:
            abort(400, game=err.__class__.__name__, errors=[str(x) for x in err.args])
        except RuntimeError as err:
            abort(409, message=str(err))

    @blp.response(204)
    def delete(self, game_id):
        """Delete game and associated rounds by id"""
        game = [game for game in Game.all() if game.id == game_id].first()
        try:
            [Round.all.remove(round) for round in game.rounds()]
            Game.all.remove(game)
        except Exception as err:
            abort(400, game=err.__class__.__name__, errors=[str(x) for x in err.args])


@blp.route("/games/<int:game_id>/rounds")
class RoundsByGameId(MethodView):
    @blp.response(200, RoundSchema(many=True))
    def get(self, game_id):
        """Get rounds by game id"""
        game = [game for game in Game.all() if game.id == game_id].first()
        return game.rounds()

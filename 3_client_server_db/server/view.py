from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import Game, Round, db
from schemas import GameSchema, GameUpdateSchema, RoundSchema
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("Guessing Game API", __name__)


@blp.route("/games")
class Games(MethodView):
    @blp.response(200, GameSchema(many=True))
    def get(self):
        """List games"""
        return db.session.scalars(db.select(Game))

    @blp.arguments(GameSchema)
    @blp.response(201, GameSchema)
    def post(self, fields):
        """Create a new game and 1st round of play"""
        try:
            game = Game(**fields)
            round = game.new_round()
            db.session.add(game, round)
            db.session.commit()
        except SQLAlchemyError as err:
            db.session.rollback()
            abort(400, game=err.__class__.__name__, errors=[str(x) for x in err.args])
        return game


@blp.route("/games/<int:game_id>")
class GamesById(MethodView):
    @blp.arguments(GameUpdateSchema)
    @blp.response(200, GameSchema)
    def patch(self, fields, game_id):
        """Update game by id.  Update current round based on the guess."""
        game = db.get_or_404(Game, game_id)
        try:
            game.update(**fields)
            if not game.is_over:
                next_round = game.new_round()
                db.session.add(next_round)
            db.session.commit()
            return game
        except SQLAlchemyError as err:
            db.session.rollback()
            abort(400, game=err.__class__.__name__, errors=[str(x) for x in err.args])
        except RuntimeError as err:
            abort(409, message=str(err))

    @blp.response(204)
    def delete(self, game_id):
        """Delete game and associated rounds by id"""
        game = db.get_or_404(Game, game_id)
        try:
            db.session.delete(game)
            db.session.commit()
        except SQLAlchemyError as err:
            db.session.rollback()
            abort(400, game=err.__class__.__name__, errors=[str(x) for x in err.args])


@blp.route("/games/<int:game_id>/rounds")
class RoundsByGameId(MethodView):
    @blp.response(200, RoundSchema(many=True))
    def get(self, game_id):
        """Get rounds by game id"""
        game = db.get_or_404(Game, game_id)
        return game.rounds

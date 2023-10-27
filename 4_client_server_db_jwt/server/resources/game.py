from functools import wraps

from db import db
from flask.views import MethodView
from flask_jwt_extended import current_user, jwt_required, verify_jwt_in_request
from flask_smorest import Blueprint, abort
from models import Game
from schemas import GameSchema, GameUpdateSchema, RoundSchema
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("Games", "games", description="Operations on games")


def game_authorized():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            game_id = kwargs.pop("game_id")
            game = db.get_or_404(Game, game_id)
            if game.user_id != current_user.id:
                abort(
                    403, message=f"You do not have permission to access Game {game.id}."
                )
            return fn(*args, game=game, **kwargs)

        return decorator

    return wrapper


@blp.route("/games")
class Games(MethodView):
    @jwt_required()
    @blp.doc(authorize=True)
    @blp.response(200, GameSchema(many=True))
    def get(self):
        """List games for authenticated user"""
        return db.session.scalars(
            db.select(Game).where(Game.user_id == current_user.id)
        )

    @jwt_required()
    @blp.doc(authorize=True)
    @blp.arguments(GameSchema)
    @blp.response(201, GameSchema)
    def post(self, fields):
        """Add a new game for authenticated user."""
        try:
            game = Game(**fields)
            game.user = current_user
            db.session.add(game)
            db.session.commit()
        except SQLAlchemyError as err:
            db.session.rollback()
            abort(400, game=err.__class__.__name__, errors=[str(x) for x in err.args])
        return game


@blp.route("/games/<int:game_id>")
class GamesById(MethodView):
    @jwt_required()
    @blp.doc(authorize=True)
    @blp.response(200, GameSchema)
    @game_authorized()
    def get(self, game):
        """Get game by id for authorized user."""
        # game = db.get_or_404(Game, game_id)
        # if game.user_id != current_user.id:
        #     abort(403, message=f"You do not have permission to access Game {game_id}.")
        # return game
        return game

    @jwt_required()
    @blp.doc(authorize=True)
    @blp.response(204)
    @game_authorized()
    def delete(self, game):
        """Delete game by id for authorized user."""
        try:
            db.session.delete(game)
            db.session.commit()
        except SQLAlchemyError as err:
            db.session.rollback()
            abort(400, game=err.__class__.__name__, errors=[str(x) for x in err.args])


@blp.route("/games/<int:game_id>/rounds")
class GameRounds(MethodView):
    @jwt_required()
    @blp.doc(authorize=True)
    @blp.response(200, RoundSchema(many=True))
    @game_authorized()
    def get(self, game):
        """List rounds by game id for authorized user."""
        return game.rounds

    @jwt_required()
    @blp.doc(authorize=True)
    @blp.response(200, GameSchema)
    @game_authorized()
    def post(self, game):
        """Add new round by game id for authorized user."""
        try:
            round = game.new_round()
            db.session.add(round)
            db.session.commit()
            return game
        except SQLAlchemyError as err:
            db.session.rollback()
            abort(400, game=err.__class__.__name__, errors=[str(x) for x in err.args])
        except RuntimeError as err:
            abort(409, message=str(err))

    @jwt_required()
    @blp.doc(authorize=True)
    @blp.arguments(GameUpdateSchema)
    @blp.response(200, GameSchema)
    @game_authorized()
    def patch(self, fields, game):
        """Update current round by game id for authorized user."""
        try:
            game.update(fields["guess"])  # update current round's status and guess
            db.session.commit()
            return game
        except SQLAlchemyError as err:
            db.session.rollback()
            abort(400, round=err.__class__.__name__, errors=[str(x) for x in err.args])
        except RuntimeError as err:
            abort(409, message=str(err))

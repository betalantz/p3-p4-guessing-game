from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import (
    jwt_required,
    current_user
)
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import Round, Game
from schemas import GameSchema, GameUpdateSchema, RoundSchema

blp = Blueprint("Games", "games", description="Operations on games")

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
        """Add a new game and 1st round of play for authenticated user."""
        try:
            game = Game(**fields)
            game.user = current_user
            db.session.add(game)
            db.session.commit()
            round = Round(game = game, range_min = game.range_min, range_max = game.range_max)
            db.session.add(round)
            db.session.commit()
        except SQLAlchemyError as err:
            db.session.rollback()
            abort(400, game=err.__class__.__name__,
                  errors=[str(x) for x in err.args])
        return game

@blp.route("/games/<int:game_id>")
class GamesById(MethodView):
    
    @jwt_required()
    @blp.doc(authorize=True)
    @blp.response(200, GameSchema)
    def get(self, game_id):
        """Get game by id for authorized user."""
        game = db.get_or_404(Game, game_id)
        if game.user_id != current_user.id:
            abort(403, message=f"You do not have permission to access Game {game_id}.") 
        return game
    
    @jwt_required()
    @blp.doc(authorize=True)
    @blp.arguments(GameUpdateSchema)
    @blp.response(200, GameSchema)
    def patch(self, fields, game_id):
        """Update game by id for authorized user."""
        game = db.get_or_404(Game, game_id)
        if game.user_id != current_user.id:
            abort(403, message=f"You do not have permission to modify Game {game_id}.") 
        if game.is_over:
            abort(409, message=f"Game {game_id} is over.")
        try:
            next_round = game.play_round(fields["guess"])
            if next_round:
                db.session.add(next_round)
            db.session.commit()  #commit status of last round and possible new round
        except SQLAlchemyError as err:
            db.session.rollback()
            abort(400, game=err.__class__.__name__,
                  errors=[str(x) for x in err.args])
        return game
    
    @jwt_required()
    @blp.doc(authorize=True)
    @blp.response(204)
    def delete(self, game_id):
        """Delete game by id for authorized user."""
        game = db.get_or_404(Game, game_id)
        if game.user_id != current_user.id:
            abort(403, message=f"You do not have permission to delete Game {game_id}.")
        try:
            db.session.delete(game)
            db.session.commit()
        except SQLAlchemyError as err:
            db.session.rollback()
            abort(400, game=err.__class__.__name__,
                  errors=[str(x) for x in err.args]) 

@blp.route("/games/<int:game_id>/rounds")
class RoundsByGameId(MethodView):
    
    @jwt_required()
    @blp.doc(authorize=True)
    @blp.response(200, RoundSchema(many=True))
    def get(self, game_id):
        """Get rounds by game id for authorized user."""
        game = db.get_or_404(Game, game_id)
        if game.user_id != current_user.id:
            abort(403, message=f"You do not have permission to access Game {game_id}.") 
        
        return game.rounds
  
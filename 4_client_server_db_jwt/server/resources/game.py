from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import Round, Game, User
from schemas import GameSchema, GameUpdateSchema, RoundSchema

blp = Blueprint("Games", "games", description="Operations on games")

@blp.route("/games")
class Games(MethodView):
    
    @blp.response(200, GameSchema(many=True))
    def get(self):
        """List games"""
        return db.session.scalars(db.select(Game))
    
    @jwt_required()
    @blp.doc(authorize=True)
    @blp.arguments(GameSchema)
    @blp.response(201, GameSchema)
    def post(self, fields):
        """Create a new game and 1st round of play for the current user"""
        try:
            user_id = get_jwt_identity()
            user = db.get_or_404(User, user_id)
            game = Game(**fields)
            game.user = user
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
    
    @blp.response(200, GameSchema)
    def get(self, game_id):
        """Get game by id"""
        return db.get_or_404(Game, game_id)
    
    @jwt_required()
    @blp.doc(authorize=True)
    @blp.arguments(GameUpdateSchema)
    @blp.response(200, GameSchema)
    def patch(self, fields, game_id):
        """Update game by id.  Update current round based on the guess. Authorization requires user to be game creator. """
        game = db.get_or_404(Game, game_id)
        user_id = get_jwt_identity()
        if game.user_id != user_id:
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
        """Delete game and associated rounds by id.  Authorization requires user to be game creator."""
        game = db.get_or_404(Game, game_id)
        user_id = get_jwt_identity()
        if game.user_id != user_id:
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
    @blp.response(200, RoundSchema(many=True))
    def get(self, game_id):
        """Get rounds by game id"""
        game = db.get_or_404(Game, game_id)
        return game.rounds
    
@blp.route("/rounds")
class Rounds(MethodView):
    
    @blp.response(200, RoundSchema(many=True))
    def get(self):
        """List rounds"""
        return db.session.scalars(db.select(Round))
  
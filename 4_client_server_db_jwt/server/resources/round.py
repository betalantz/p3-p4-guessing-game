from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import (
    jwt_required,
    current_user
)
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import Round
from schemas import RoundSchema, RoundUpdateSchema

blp = Blueprint("Rounds", "rounds", description="Operations on rounds")

@blp.route("/rounds/<int:round_id>")
class RoundById(MethodView):

    @jwt_required()
    @blp.doc(authorize=True)
    @blp.arguments(RoundUpdateSchema)
    @blp.response(200, RoundSchema)
    def patch(self, fields, round_id):
        """Update round by id for authorized user."""
        round = db.get_or_404(Round, round_id)
        if round.game.user_id != current_user.id:
            abort(403, message=f"You do not have permission to modify Round {round_id}.") 
        try:
            round.update(fields["guess"])  #update status and guess
            db.session.commit() 
            return round
        except SQLAlchemyError as err:
            db.session.rollback()
            abort(400, round=err.__class__.__name__,
                  errors=[str(x) for x in err.args])
        except RuntimeError as err:
            abort(409, message=str(err))

  
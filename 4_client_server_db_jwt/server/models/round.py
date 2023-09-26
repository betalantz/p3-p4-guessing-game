from db import db

class Round(db.Model):
    """Round model"""
    __tablename__ = "rounds"
    id = db.Column(db.Integer, primary_key=True)
    range_min = db.Column(db.Integer, nullable=False)
    range_max = db.Column(db.Integer, nullable=False)
    guess = db.Column(db.Integer)
    status = db.Column(db.String)

    game_id = db.Column(db.Integer, db.ForeignKey("games.id"), nullable=False)
    game = db.relationship("Game", back_populates="rounds")

    __table_args__ = (
        db.CheckConstraint("range_min <= range_max", name="min_max_range"),
    )

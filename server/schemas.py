from marshmallow import Schema, fields, validates_schema, validates,ValidationError
from models import Game

class RoundSchema(Schema):
    id = fields.Int()
    game_id = fields.Int()
    minValue = fields.Int()
    maxValue = fields.Int()
    guess = fields.Int()
    status = fields.String()
    
    @validates("game_id")
    def game_foreign_key(self, value):
        """game_id is valid foreign key"""
        if Game.all.get(value) is None:
            raise ValidationError(f"Foreign key violation for game_id {value}.")

    
class GameSchema(Schema):
    id = fields.Int(dump_only = True)
    minValue = fields.Int(required=True)
    maxValue = fields.Int(required=True)
    secretNumber = fields.Int(dump_only = True)
    isOver = fields.Boolean(dump_only = True)
    @validates_schema
    def validate_numbers(self, data, **kwargs):
        minVal = data["minValue"]
        maxVal = data["maxValue"]
        if minVal >= maxVal:
            raise ValidationError(f"minValue {minVal} must be less than maxValue {maxVal}.")
    
class GameUpdateSchema(Schema):
    guess = fields.Int(required=True)

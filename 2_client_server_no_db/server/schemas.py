from marshmallow import Schema, fields, pre_dump, post_load, validates_schema, ValidationError, validate
from models import Round, Game, DifficultyLevel, GuessStatus

class RoundSchema(Schema):
    __model__ = Round
    # Use 'only' or 'exclude' to avoid infinite recursion with two-way nested fields.
    game = fields.Nested("GameSchema", only=("id",))
    range_min = fields.Int()
    range_max = fields.Int()
    guess = fields.Int()
    status = fields.Str(validate=validate.OneOf([status for status in GuessStatus.__members__.values()]))  #["correct", "low", "high", "invalid"]
    
    
class GameSchema(Schema):
    __model__ = Game
    id = fields.Str(dump_only = True)
    difficulty = fields.Str(required=True, validate=validate.OneOf([level for level in DifficultyLevel.__members__.values()]))  #["easy", "hard"]
    range_min = fields.Int(required=True)
    range_max = fields.Int(required=True)
    secret_number = fields.Int(dump_only = True)
    is_over = fields.Boolean(dump_only = True)
    rounds = fields.Nested(RoundSchema, many=True, dump_only = True)
    
    # Compute list of rounds associated with this game prior to serialization
    @pre_dump()
    def get_data(self, data, **kwargs):
        data.rounds = data.get_rounds()
        return data
    
    @validates_schema
    def validate_range(self, data, **kwargs):
        range_min = data["range_min"]
        range_max = data["range_max"]
        if range_min > range_max:
            raise ValidationError(f"error: range_min {range_min} is greater than range_max {range_max}")
        
class GameUpdateSchema(Schema):
    guess = fields.Int(required=True)

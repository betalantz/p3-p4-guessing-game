from marshmallow import Schema, fields, pre_dump, post_load, validates_schema, ValidationError, validate
from models import Round, Game, DifficultyLevel, GuessStatus

class RoundSchema(Schema):
    __model__ = Round
    # Use 'only' or 'exclude' to avoid infinite recursion with two-way nested fields.
    id = fields.Int(dump_only = True)
    game = fields.Nested("GameSchema", only=("id",))
    min_value = fields.Int()
    max_value = fields.Int()
    guess = fields.Int()
    status = fields.Str(validate=validate.OneOf([status for status in GuessStatus.__members__.values()]))  #["correct", "low", "high", "invalid"]
    
    
class GameSchema(Schema):
    __model__ = Game
    id = fields.Int(dump_only = True)
    difficulty = fields.Str(required=True, validate=validate.OneOf([level for level in DifficultyLevel.__members__.values()]))  #["easy", "hard"]
    min_value = fields.Int(required=True)
    max_value = fields.Int(required=True)
    secret_number = fields.Int(dump_only = True)
    is_over = fields.Boolean(dump_only = True)
    rounds = fields.Nested(RoundSchema, many=True, dump_only = True)
    
    @validates_schema
    def validate_range(self, data, **kwargs):
        min_val = data["min_value"]
        max_val = data["max_value"]
        if min_val > max_val:
            raise ValidationError(f"min_value {min_val} must be less than or equal to max_value {max_val}.")
    
class GameUpdateSchema(Schema):
    guess = fields.Int(required=True)

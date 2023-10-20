from marshmallow import Schema, fields, validates_schema, ValidationError, validate
from models import DifficultyLevel, GuessStatus
    
class RoundSchema(Schema):
    id = fields.Int(dump_only = True)
    #game = fields.Nested("GameSchema", only=("id",))
    game_id = fields.Int()
    range_min = fields.Int()
    range_max = fields.Int()
    number = fields.Int()
    guess = fields.Int()
    status = fields.Str(validate=validate.OneOf([status for status in GuessStatus.__members__.values()]))  #["correct", "low", "high", "invalid"]

class GameSchema(Schema):
    id = fields.Int(dump_only = True)
    difficulty = fields.Str(required=True, validate=validate.OneOf([level for level in DifficultyLevel.__members__.values()]))  #["easy", "hard"]
    range_min = fields.Int(required=True)
    range_max = fields.Int(required=True)
    secret_number = fields.Int(dump_only = True)
    is_over = fields.Boolean(dump_only = True)
    #user = fields.Nested("UserSchema", only=("id",), dump_only = True)
    user_id = fields.Int(dump_only = True)
    #rounds = fields.Nested(RoundSchema, many=True, dump_only = True)
    number_of_rounds = fields.Function(lambda obj: len(obj.rounds), dump_only = True)
    
    
    @validates_schema
    def validate_range(self, data, **kwargs):
        range_min = data["range_min"]
        range_max = data["range_max"]
        if range_min > range_max:
            raise ValidationError(f"error: range_min {range_min} is greater than range_max {range_max}")    

class RoundUpdateSchema(Schema):
    guess = fields.Int(required=True)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    #games = fields.Nested(GameSchema, many=True, dump_only = True)
    
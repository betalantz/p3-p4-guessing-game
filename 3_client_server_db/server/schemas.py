# from models import DIFFICULTY_LEVEL, GUESS_STATUS
import models
from marshmallow import Schema, ValidationError, fields, validate, validates_schema


class RoundSchema(Schema):
    # Use 'only' or 'exclude' to avoid infinite recursion with two-way nested fields.
    id = fields.Int(dump_only=True)
    #
    game = fields.Nested("GameSchema", dump_only=True)
    range_min = fields.Int()
    range_max = fields.Int()
    number = fields.Int()
    guess = fields.Int()
    status = fields.Str(
        validate=validate.OneOf([status for status in models.GUESS_STATUS.values()])
    )  # ["correct", "low", "high", "invalid"]


class GameSchema(Schema):
    id = fields.Int(dump_only=True)
    difficulty = fields.Str(
        required=True,
        validate=validate.OneOf([level for level in models.DIFFICULTY_LEVEL.values()]),
    )  # ["easy", "hard"]
    range_min = fields.Int(required=True)
    range_max = fields.Int(required=True)
    secret_number = fields.Int(dump_only=True)
    is_over = fields.Boolean(dump_only=True)
    current_round = fields.Nested("RoundSchema", exclude=("game",), dump_only=True)
    number_of_rounds = fields.Int(dump_only=True)

    @validates_schema
    def validate_range(self, data, **kwargs):
        range_min = data["range_min"]
        range_max = data["range_max"]
        if range_min > range_max:
            raise ValidationError(
                f"error: range_min {range_min} is greater than range_max {range_max}"
            )


class GameUpdateSchema(Schema):
    guess = fields.Int(required=True)
    round_id = fields.Int(required=True)

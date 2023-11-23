import logging

import ipdb
from marshmallow import (
    Schema,
    ValidationError,
    fields,
    pre_dump,
    validate,
    validates_schema,
)
from models import DifficultyLevel, GuessStatus

logger = logging.getLogger(__name__)


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
        validate=validate.OneOf([status for status in GuessStatus.__members__.values()])
    )  # ["correct", "low", "high", "invalid"]


class GameSchema(Schema):
    id = fields.Int(dump_only=True)
    difficulty = fields.Str(
        required=True,
        validate=validate.OneOf(
            [level for level in DifficultyLevel.__members__.values()]
        ),
    )  # ["easy", "hard"]
    range_min = fields.Int(required=True)
    range_max = fields.Int(required=True)
    secret_number = fields.Int(dump_only=True)
    is_over = fields.Boolean(dump_only=True)
    # rounds = fields.Nested(RoundSchema, many=True, dump_only = True)
    current_round = fields.Nested("RoundSchema", exclude=("game",), dump_only=True)
    number_of_rounds = fields.Int(dump_only=True)
    # number_of_rounds = fields.Function(lambda obj: len(obj.rounds), dump_only=True)

    # Compute current round prior to serialization
    # def get_current_round(self, obj):
    #     # print(type(obj))
    #     return obj.current_round()

    # def get_number_of_rounds(self, obj):
    #     # ipdb.set_trace()
    #     logger.debug(f"get_number_of_rounds called with: {obj}")
    #     return len(obj.rounds)

    # @pre_dump()
    # def get_data(self, data, **kwargs):
    #     data.current_round = data.current_round()
    #     return data

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

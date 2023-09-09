from marshmallow import Schema, fields, validates_schema, ValidationError
    
class RoundSchema(Schema):
    minValue = fields.Int()
    maxValue = fields.Int()
    guess = fields.Int()
    status = fields.String()
    
class GameSchema(Schema):
    id = fields.Int(dump_only = True)
    minValue = fields.Int(required=True)
    maxValue = fields.Int(required=True)
    secretNumber = fields.Int(dump_only = True)
    isOver = fields.Boolean(dump_only = True)
    rounds = fields.Nested(RoundSchema, dump_only = True, many=True)
    @validates_schema
    def validate_numbers(self, data, **kwargs):
        minVal = data["minValue"]
        maxVal = data["maxValue"]
        if minVal >= maxVal:
            raise ValidationError(f"minValue {minVal} must be less than maxValue {maxVal}.")

    
class GameUpdateSchema(Schema):
    guess = fields.Int(required=True)

import pytest
from lib.models import DifficultyLevel, Game, GuessStatus, Round
from lib.schemas import GameSchema, RoundSchema
from marshmallow import ValidationError, fields, validate


class TestRoundSchema:
    """
    The RoundSchema class in schemas.py
    """

    @pytest.fixture
    def round_schema(self):
        return RoundSchema()

    def test_model(self, round_schema):
        """
        has a __model__ attribute set to the Round class.
        """
        assert round_schema.__model__ == Round

    def test_id(self, round_schema):
        """
        has an id field of type Str.
        """
        assert isinstance(round_schema.fields["id"], fields.Str)
        assert round_schema.fields["id"].dump_only is True

    def test_game(self, round_schema):
        """
        has a game field of type Nested, with reference to GameSchema and only the id field.
        """
        assert isinstance(round_schema.fields["game"], fields.Nested)
        assert round_schema.fields["game"].nested == "GameSchema"
        assert round_schema.fields["game"].only == ("id",)

    def test_range_min(self, round_schema):
        """
        has a range_min field of type Int.
        """
        assert isinstance(round_schema.fields["range_min"], fields.Int)

    def test_range_max(self, round_schema):
        """
        has a range_max field of type Int.
        """
        assert isinstance(round_schema.fields["range_max"], fields.Int)

    def test_guess(self, round_schema):
        """
        has a guess field of type Int.
        """
        assert isinstance(round_schema.fields["guess"], fields.Int)

    def test_status(self, round_schema):
        """
        has a status field of type Str.
        """
        assert isinstance(round_schema.fields["status"], fields.Str)
        assert isinstance(round_schema.fields["status"].validate, validate.OneOf)
        assert round_schema.fields["status"].validate.choices == [
            status for status in GuessStatus.__members__.values()
        ]


class TestGameSchema:
    """
    The GameSchema class in schemas.py
    """

    @pytest.fixture
    def game_schema(self):
        return GameSchema()

    def test_model(self, game_schema):
        """
        has a __model__ attribute set to the Game class.
        """
        assert game_schema.__model__ == Game

    def test_id(self, game_schema):
        """
        has an id field of type Str.
        """
        assert isinstance(game_schema.fields["id"], fields.Str)
        assert game_schema.fields["id"].dump_only is True

    def test_difficulty(self, game_schema):
        """
        has a difficulty field of type Str.
        """
        assert isinstance(game_schema.fields["difficulty"], fields.Str)
        assert game_schema.fields["difficulty"].required is True
        assert isinstance(game_schema.fields["difficulty"].validate, validate.OneOf)
        assert game_schema.fields["difficulty"].validate.choices == [
            level for level in DifficultyLevel.__members__.values()
        ]

    def test_range_min(self, game_schema):
        """
        has a range_min field of type Int.
        """
        assert isinstance(game_schema.fields["range_min"], fields.Int)
        assert game_schema.fields["range_min"].required is True

    def test_range_max(self, game_schema):
        """
        has a range_max field of type Int.
        """
        assert isinstance(game_schema.fields["range_max"], fields.Int)
        assert game_schema.fields["range_max"].required is True

    def test_secret_number(self, game_schema):
        """
        has a secret_number field of type Int.
        """
        assert isinstance(game_schema.fields["secret_number"], fields.Int)
        assert game_schema.fields["secret_number"].dump_only is True

    def test_is_over(self, game_schema):
        """
        has an is_over field of type Boolean.
        """
        assert isinstance(game_schema.fields["is_over"], fields.Boolean)
        assert game_schema.fields["is_over"].dump_only is True

    def test_rounds(self, game_schema):
        """
        has a rounds field of type Nested, with reference to RoundSchema and many=True.
        """
        assert isinstance(game_schema.fields["rounds"], fields.Nested)
        assert game_schema.fields["rounds"].nested == RoundSchema
        assert game_schema.fields["rounds"].many is True

    def test_pre_dump(self, test_game, game_schema):
        """
        has a pre_dump decorated method called get_data that sets
        the rounds attribute to the result of get_rounds.
        """
        assert hasattr(game_schema, "get_data")
        assert game_schema.get_data.__name__ == "get_data"
        game_schema.get_data(test_game)
        assert test_game.rounds == test_game.get_rounds()

    def test_validate_range(self, game_schema):
        """
        has a validates_schema decorated method called validate_range that
        raises a ValidationError if range_min is greater than range_max.
        """
        assert hasattr(game_schema, "validate_range")
        assert game_schema.validate_range.__name__ == "validate_range"
        with pytest.raises(ValidationError) as e:
            game_schema.validate_range({"range_min": 10, "range_max": 1})
        assert str(e.value) == "error: range_min 10 is greater than range_max 1"

    @pytest.fixture
    def game_data(self):
        return {
            "difficulty": "easy",
            "range_min": 1,
            "range_max": 10,
        }

    def test_post_load(self, game_schema, game_data):
        """
        has a post_load decorated method called make_object that returns a Game object.
        """
        assert hasattr(game_schema, "make_object")
        assert game_schema.make_object.__name__ == "make_object"
        game = game_schema.make_object(game_data)
        assert isinstance(game, Game)
        assert game.difficulty == DifficultyLevel.EASY
        assert game.range_min == 1
        assert game.range_max == 10
        assert game.is_over is False

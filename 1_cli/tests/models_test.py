import pytest
from lib.models import DifficultyLevel, Game, GuessStatus, Round


class TestGuessStatus:
    """
    The GuessStatus enumeration in models.py
    """

    def test_correct(self):
        """
        has a member called CORRECT.
        """
        assert GuessStatus.CORRECT is not None
        assert GuessStatus.CORRECT.name == "CORRECT"

    def test_high(self):
        """
        has a member called HIGH.
        """
        assert GuessStatus.HIGH is not None
        assert GuessStatus.HIGH.name == "HIGH"

    def test_low(self):
        """
        has a member called LOW.
        """
        assert GuessStatus.LOW is not None
        assert GuessStatus.LOW.name == "LOW"

    def test_invalid(self):
        """
        has a member called INVALID.
        """
        assert GuessStatus.INVALID is not None
        assert GuessStatus.INVALID.name == "INVALID"

    def test_4_members(self):
        """
        has exactly four members.
        """
        assert len(GuessStatus.__members__) == 4

    def test_auto_assigns_values(self):  # new test
        """
        assigns auto values to members.
        """
        assert isinstance(GuessStatus.CORRECT.value, str)
        assert isinstance(GuessStatus.HIGH.value, str)
        assert isinstance(GuessStatus.LOW.value, str)
        assert isinstance(GuessStatus.INVALID.value, str)
        assert GuessStatus.CORRECT.value != GuessStatus.HIGH.value
        assert GuessStatus.CORRECT.value != GuessStatus.LOW.value
        assert GuessStatus.CORRECT.value != GuessStatus.INVALID.value
        assert GuessStatus.HIGH.value != GuessStatus.LOW.value


class TestDifficultyLevel:
    """
    The DifficultyLevel enumeration in models.py
    """

    def test_easy(self):
        """
        has a member called EASY.
        """
        assert DifficultyLevel.EASY is not None
        assert DifficultyLevel.EASY.name == "EASY"

    def test_hard(self):
        """
        has a member called HARD.
        """
        assert DifficultyLevel.HARD is not None
        assert DifficultyLevel.HARD.name == "HARD"

    def test_2_members(self):
        """
        has exactly two members.
        """
        assert len(DifficultyLevel.__members__) == 2

    def test_auto_assigns_values(self):  # new test
        """
        assigns auto values to members.
        """
        assert isinstance(DifficultyLevel.EASY.value, str)
        assert isinstance(DifficultyLevel.HARD.value, str)
        assert DifficultyLevel.EASY.value != DifficultyLevel.HARD.value


class TestRound:
    """
    The Round class in models.py
    """

    def test_all(self):
        """
        has an attribute called all that is a list.
        """
        assert hasattr(Round, "all")
        assert isinstance(Round.all, list)

    def test_all_starts_empty(self):
        """
        all is an empty list.
        """
        assert Round.all == []

    def test_init(self, test_game, test_round):
        """
        initializes with a game, range_min, and range_max.
        """
        assert test_round.game == test_game
        assert test_round.range_min == 1
        assert test_round.range_max == 10

    def test_init_adds_to_all(self, test_round):
        """
        adds itself to the all list.
        """
        assert test_round in Round.all

    def test_init_assigns_unique_id(self, test_round):
        """
        assigns a unique id.
        """
        assert test_round.id is not None
        assert test_round.id != ""

    def test_init_assigns_id_as_string(self, test_round):
        """
        assigns the id as a string.
        """
        assert isinstance(test_round.id, str)

    def test_init_assigns_unique_id_each_time(self, test_game):
        """
        assigns a unique id each time.
        """
        round1 = Round(test_game, 1, 10)
        round2 = Round(test_game, 1, 10)
        assert round1.id != round2.id

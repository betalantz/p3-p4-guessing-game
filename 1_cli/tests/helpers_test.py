import pytest
from lib.helpers import exit_program, new_game, response_message
from lib.models import Game, GuessStatus


class TestExitProgram:
    """
    The exit_program function in helpers.py
    """

    def test_exit(self):
        """
        calls exit() and raises SystemExit.
        """
        with pytest.raises(SystemExit):  # Expect the program to exit
            exit_program()

    def test_prints_goodbye(self, capsys):
        """
        prints "Goodbye!".
        """
        with pytest.raises(SystemExit):
            exit_program()
        captured = capsys.readouterr()
        assert captured.out.strip() == "Goodbye!"


class TestResponseMessage:
    """
    The response_message function in helpers.py
    """

    @pytest.mark.parametrize(
        "status, expected",
        [
            (GuessStatus.CORRECT, "1 is correct!"),
            (GuessStatus.LOW, "1 is too low."),
            (GuessStatus.HIGH, "1 is too high."),
            (GuessStatus.INVALID, "1 is outside the range 1..10."),
        ],
    )
    def test_returns_correct_message(self, test_round, status, expected):
        """
        returns the correct message based on the status.
        """
        test_round.status = status
        assert response_message(test_round) == expected


class TestNewGame:
    """
    The new_game function in helpers.py
    """

    @pytest.mark.parametrize(
        "inputs, expected",
        [
            (["easy", "1", "10", "5"], "5 is correct!"),
            (["easy", "1", "10", "1", "5"], "5 is correct!"),
            (["easy", "1", "10", "1", "2", "5"], "5 is correct!"),
            (["easy", "1", "10", "1", "2", "3", "5"], "5 is correct!"),
            (["easy", "1", "10", "10", "5"], "5 is correct!"),
            (["easy", "1", "10", "10", "9", "5"], "5 is correct!"),
            (["easy", "1", "10", "10", "9", "8", "5"], "5 is correct!"),
            (["easy", "1", "10", "10", "9", "8", "7", "5"], "5 is correct!"),
            (["easy", "1", "10", "10", "9", "8", "7", "6", "5"], "5 is correct!"),
            (
                ["easy", "1    ", "10", "5"],
                "5 is correct!",
            ),  # Test leading whitespace 1
        ],
    )
    def test_easy_new_game(self, inputs, expected, capsys, mocker):
        """
        plays a game of "easy" difficulty and wins.
        """
        input_mock = mocker.patch("builtins.input", side_effect=inputs)
        mocker.patch("lib.models.randint", return_value=5)  # Mock the secret number
        new_game()
        captured = capsys.readouterr()
        output_lines = captured.out.splitlines()
        for idx, input in list(enumerate(inputs)):
            if idx > 2:
                output_line = output_lines[idx - 3]
                if int(input) < 5:
                    assert "too low" in output_line
                elif int(input) > 5:
                    assert "too high" in output_line
                elif input == "5":
                    assert expected in output_line

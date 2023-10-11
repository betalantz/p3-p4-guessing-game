import pytest
from lib.helpers import exit_program


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
            ("CORRECT", "1 is correct!"),
            ("LOW", "1 is too low."),
            ("HIGH", "1 is too high."),
            ("INVALID", "1 is outside the range 1..1."),
        ],
    )
    def test_returns_correct_message(self, status, expected):
        """
        returns the correct message based on the status.
        """
        round = GuessRound(guess=1, status=status)
        assert response_message(round) == expected

import unittest
from io import StringIO
from unittest.mock import patch

from lib.cli import main, menu


class TestMain(unittest.TestCase):

    """The main function in cli.py"""

    @patch("builtins.input", side_effect=["0"])
    def test_exit(self, input_mock):
        """
        calls exit_program by simulating user input "0".
        """
        with self.assertRaises(SystemExit):  # Expect the program to exit
            main()

    @patch("lib.cli.new_game")
    @patch("builtins.input", side_effect=["1", "0"])
    def test_main_calls_new_game(
        self, input_mock, new_game_mock
    ):  # Note the order of the arguments
        """
        calls new_game when the first input is "1".
        """
        try:  # Catch SystemExit to avoid exiting the test
            main()
        except SystemExit:
            pass
        new_game_mock.assert_called_once()

    @patch("lib.cli.list_games")
    @patch("builtins.input", side_effect=["2", "0"])
    def test_main_calls_list_games(
        self, input_mock, list_games_mock
    ):  # Note the order of the arguments
        """
        calls list_games when the first input is "2".
        """
        try:  # Catch SystemExit to avoid exiting the test
            main()
        except SystemExit:
            pass
        list_games_mock.assert_called_once()


class TestMenu(unittest.TestCase):
    @patch("sys.stdout", new_callable=StringIO)
    def test_menu(self, mock_stdout):
        """
        Test the menu function by capturing its output.
        """
        menu()
        output = mock_stdout.getvalue()
        self.assertIn("Please select an option:", output)
        self.assertIn("0. Exit the program", output)
        self.assertIn("1. Play new game", output)
        self.assertIn("2: List all games", output)
        self.assertIn("3: List game by id", output)
        self.assertIn("4: List all rounds", output)
        self.assertIn("5: List rounds by game id", output)

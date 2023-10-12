from io import StringIO
from unittest.mock import patch

import pytest
from lib.cli import main, menu


class TestMain:
    """
    The main function in cli.py
    """

    @patch("lib.cli.exit_program", side_effect=SystemExit)
    @patch("builtins.input", side_effect=["0", "0"])
    def test_main_calls_exit_program(
        self, input_mock, exit_program_mock
    ):  # Note the order of the arguments
        """
        calls exit_program when the first input is "0".
        """
        with pytest.raises(SystemExit):  # Expect the program to exit
            main()
        exit_program_mock.assert_called_once()

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

    @patch("lib.cli.list_game_by_id")
    @patch("builtins.input", side_effect=["3", "0"])
    def test_main_calls_list_game_by_id(
        self, input_mock, list_game_by_id_mock
    ):  # Note the order of the arguments
        """
        calls list_game_by_id when the first input is "3".
        """
        try:  # Catch SystemExit to avoid exiting the test
            main()
        except SystemExit:
            pass
        list_game_by_id_mock.assert_called_once()

    @patch("lib.cli.list_rounds")
    @patch("builtins.input", side_effect=["4", "0"])
    def test_main_calls_list_rounds(
        self, input_mock, list_rounds_mock
    ):  # Note the order of the arguments
        """
        calls list_rounds when the first input is "4".
        """
        try:  # Catch SystemExit to avoid exiting the test
            main()
        except SystemExit:
            pass
        list_rounds_mock.assert_called_once()

    @patch("lib.cli.list_rounds_by_game_id")
    @patch("builtins.input", side_effect=["5", "0"])
    def test_main_calls_list_rounds_by_game_id(
        self, input_mock, list_rounds_by_game_id_mock
    ):  # Note the order of the arguments
        """
        calls list_rounds_by_game_id when the first input is "5".
        """
        try:  # Catch SystemExit to avoid exiting the test
            main()
        except SystemExit:
            pass
        list_rounds_by_game_id_mock.assert_called_once()

    @patch("sys.stdout", new_callable=StringIO)
    @patch("builtins.input", side_effect=["z", "0"])
    def test_main_catches_invalid_inputs(
        self, input_mock, mock_stdout
    ):  # Note the order of the arguments
        """
        prints "Invalid choice" when the first input is not "0", "1", "2", "3", "4", or "5".
        """
        try:  # Catch SystemExit to avoid exiting the test
            main()
        except SystemExit:
            pass
        output = mock_stdout.getvalue()
        assert "Invalid choice" in output


class TestMenu:
    """
    The menu function in cli.py
    """

    @patch("sys.stdout", new_callable=StringIO)
    def test_menu(self, mock_stdout):
        """
        prints the required output.
        """
        menu()
        output = mock_stdout.getvalue()
        assert "Please select an option:" in output
        assert "0. Exit the program" in output
        assert "1. Play new game" in output
        assert "2: List all games" in output
        assert "3: List game by id" in output
        assert "4: List all rounds" in output
        assert "5: List rounds by game id" in output

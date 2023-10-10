import unittest
from unittest.mock import patch

from lib.cli import main


class TestMain(unittest.TestCase):
    @patch("builtins.input", side_effect=["0"])
    def test_main(self, input_mock):
        """
        Test the main function by simulating user input.
        """
        with self.assertRaises(SystemExit):  # Expect the program to exit
            main()

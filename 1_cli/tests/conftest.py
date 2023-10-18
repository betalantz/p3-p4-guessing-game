#!/usr/bin/env python3

import pytest
from lib.models import Game, Round


def pytest_itemcollected(item):
    par = item.parent.obj
    node = item.obj
    pref = par.__doc__.strip() if par.__doc__ else par.__class__.__name__
    suf = node.__doc__.strip() if node.__doc__ else node.__name__
    if pref or suf:
        item._nodeid = " ".join((pref, suf))


@pytest.fixture(autouse=True)
def reset_game():
    Game.all = {}
    Round.all = []


# The autouse=True argument means that this fixture will be automatically used by all tests.
# The reset_game function is called before each test to reset the Game and Round classes to their initial state.


@pytest.fixture
def test_game():
    game = Game(difficulty="easy", range_min=1, range_max=10)
    game.secret_number = 5
    return game


@pytest.fixture
def test_round(test_game):
    round = test_game.get_rounds()[-1]
    round.guess = 1
    return round

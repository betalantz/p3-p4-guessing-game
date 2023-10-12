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


@pytest.fixture
def test_game():
    game = Game(difficulty="easy", range_min=1, range_max=10)
    game.secret_number = 5
    return game


@pytest.fixture
def test_round():
    game = Game(difficulty="easy", range_min=1, range_max=10)
    round = game.get_rounds()[-1]
    round.guess = 1
    return round

import pytest

from app.models.game import Game, Round
from tests.unit.models.conftest import TEST_USER1, TEST_USER2


@pytest.mark.parametrize(
    "rounds",
    (
        [],
        [
            Round(id=1, winner=None),
        ],
        [
            Round(id=1, winner=TEST_USER1),
            Round(id=2, winner=TEST_USER2),
        ],
        [
            Round(id=1, winner=TEST_USER1),
            Round(id=2, winner=TEST_USER2),
            Round(id=3, winner=None),
        ],
    ),
)
def test_game_winner_is_None(rounds):
    game: Game = Game(id=1)
    game.rounds.extend(rounds)
    assert game.get_winner() is None


@pytest.mark.parametrize(
    "rounds, expected",
    (
        (
            [
                Round(id=1, winner=TEST_USER1),
            ],
            TEST_USER1,
        ),
        (
            [
                Round(id=1, winner=TEST_USER1),
                Round(id=1, winner=TEST_USER1),
            ],
            TEST_USER1,
        ),
        (
            [
                Round(id=1, winner=TEST_USER1),
                Round(id=2, winner=TEST_USER2),
                Round(id=3, winner=TEST_USER2),
            ],
            TEST_USER2,
        ),
    ),
)
def test_game_winner(rounds, expected):
    game: Game = Game(id=1)
    game.rounds.extend(rounds)
    assert game.get_winner() == expected

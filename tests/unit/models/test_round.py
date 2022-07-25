import pytest

from app.models.game import Move, Round

from .conftest import PAPER, ROCK, SCISSORS, TEST_USER1, TEST_USER2


@pytest.mark.parametrize(
    "move1,move2",
    (
        (
            Move(
                user=TEST_USER1,
                option=ROCK,
            ),
            None,
        ),
        (
            Move(
                user=TEST_USER1,
                option=ROCK,
            ),
            Move(
                user=TEST_USER2,
                option=ROCK,
            ),
        ),
    ),
)
def test_round_winner_is_None(move1, move2):
    round: Round = Round(id=1, game_id=1)
    round.moves.append(move1)
    if move2:
        round.moves.append(move2)
    assert round.get_winner() is None


@pytest.mark.parametrize(
    "move1,move2,expected",
    (
        (
            Move(
                user=TEST_USER1,
                option=ROCK,
            ),
            Move(
                user=TEST_USER2,
                option=PAPER,
            ),
            TEST_USER2,
        ),
        (
            Move(
                user=TEST_USER1,
                option=ROCK,
            ),
            Move(
                user=TEST_USER2,
                option=SCISSORS,
            ),
            TEST_USER1,
        ),
        (
            Move(
                user=TEST_USER1,
                option=PAPER,
            ),
            Move(
                user=TEST_USER2,
                option=SCISSORS,
            ),
            TEST_USER2,
        ),
    ),
)
def test_round_winner(move1, move2, expected):
    round: Round = Round(id=1, game_id=1)
    round.moves.append(move1)
    round.moves.append(move2)
    assert round.get_winner() == expected

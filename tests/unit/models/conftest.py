from app.models.option import Option
from app.models.user import User

TEST_USER1: User = User(id=1, username="test1")
TEST_USER2: User = User(id=2, username="test2")

ROCK: Option = Option(title="rock")
PAPER: Option = Option(title="paper")
SCISSORS: Option = Option(title="scissors")
ROCK.beats.append(SCISSORS)
PAPER.beats.append(ROCK)
SCISSORS.beats.append(PAPER)

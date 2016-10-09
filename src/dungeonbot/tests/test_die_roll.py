# from flask_testing import TestCase
from dungeonbot.conftest import BaseTest
from dungeonbot.plugins.helpers.die_roll import DieRoll


class DieRollTest(BaseTest):
    """Test Helper file: die_roll."""

    def test_basic_init(self):
        """Test attributes of DieRoll object created with a basic roll string."""
        roll = DieRoll("1d20", flag=None)
        assert roll.roll_str == "1d20"
        assert roll.operator == "+"
        assert roll.action == roll.roll_die
        assert roll.modifier == 0
        assert roll.message == ""
        assert roll.number == 1
        assert roll.sides == 20
        assert roll.min_roll == roll.number
        assert roll.max_roll == roll.sides * roll.number

    def test_a_init(self):
        """Test attributes of DieRoll object created with a roll string with advantage."""
        roll = DieRoll("1d20", flag="a")
        assert roll.roll_str == "1d20"
        assert roll.operator == "+"
        assert roll.action == roll.advantage
        assert roll.modifier == 0
        assert roll.message == ""
        assert roll.number == 1
        assert roll.sides == 20
        assert roll.min_roll == roll.number
        assert roll.max_roll == roll.sides * roll.number

    def test_d_init(self):
        """Test attribuetes of DieRoll object created with a roll string with disadvantage."""
        roll = DieRoll("1d20", flag="d")
        assert roll.roll_str == "1d20"
        assert roll.operator == "+"
        assert roll.action == roll.disadvantage
        assert roll.modifier == 0
        assert roll.message == ""
        assert roll.number == 1
        assert roll.sides == 20
        assert roll.min_roll == roll.number
        assert roll.max_roll == roll.sides * roll.number

    def test_positive_init(self):
        """Test attributes of DieRoll object created with a roll string with a plus."""
        roll = DieRoll("1d20+32", flag=None)
        assert roll.roll_str == "1d20+32"
        assert roll.operator == "+"
        assert roll.action == roll.roll_die
        assert roll.modifier == 32
        assert roll.message == ""
        assert roll.number == 1
        assert roll.sides == 20
        assert roll.min_roll == roll.number
        assert roll.max_roll == roll.sides * roll.number

    def test_negative_init(self):
        """Test attributes of DieRoll object created with a roll string with a minus."""
        roll = DieRoll("1d20-32", flag=None)
        assert roll.roll_str == "1d20-32"
        assert roll.operator == "-"
        assert roll.action == roll.roll_die
        assert roll.modifier == -32
        assert roll.message == ""
        assert roll.number == 1
        assert roll.sides == 20
        assert roll.min_roll == roll.number
        assert roll.max_roll == roll.sides * roll.number

    def test_negative_with_flag(self):
        """Test attributes with a minus and a flag."""
        roll = DieRoll("1d20-32", flag="d")
        assert roll.roll_str == "1d20-32"
        assert roll.operator == "-"
        assert roll.action == roll.disadvantage
        assert roll.modifier == -32
        assert roll.message == ""
        assert roll.number == 1
        assert roll.sides == 20
        assert roll.min_roll == roll.number
        assert roll.max_roll == roll.sides * roll.number

    def test_print_results(self):
        """Test print results, basic."""
        roll = DieRoll("1d20", flag=None)
        roll_result = 10
        message = "*[ 10 ]* _(1d20 = 10 + 0) (min 1, max 20) _"
        assert roll.print_results(roll_result) == message

    def test_print_results_named(self):
        """Test print results with a name."""
        roll = DieRoll("1d20", flag=None)
        roll_result = 10
        name = "blue"
        message = "*[ 10 ]* _(1d20 = 10 + 0) (min 1, max 20) _ with blue"
        assert roll.print_results(roll_result, name=name) == message

    def test_roll_die(self):
        """Test method roll_die."""
        roll = DieRoll("1d20-1", flag=None)
        assert roll.action == roll.roll_die
        assert roll.roll_die() in range(roll.min_roll, roll.max_roll + 1)

    def test_advantage(self):
        """Test method advantage."""
        roll = DieRoll("1d20+1", flag="a")
        assert roll.action == roll.advantage
        assert roll.advantage() in range(roll.min_roll, roll.max_roll + 1)

    def test_disadvantage(self):
        """Test disadvantage method."""
        roll = DieRoll("1d20+1", flag="d")
        assert roll.action == roll.disadvantage
        assert roll.disadvantage() in range(roll.min_roll, roll.max_roll + 1)

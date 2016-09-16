class DieRoll(object):
    """Roll object that parses roll string and calls appropriate function."""

    def __init__(self, roll_str):
        """Initialize Die roll object by breaking apart roll string."""
        self.roll_str = roll = roll_str.lstrip("-")
        self.operator = "+"
        # make into a property?
        self.action = self.roll_die

        self.modifier = 0
        self.message = ""
        valid_operators = ["+", "-"]
        valid_flags = {
            "a": self.advantage,
            "d": self.disadvantage
        }

        for f in valid_flags:
            if roll.startswith(f):
                self.action = valid_flags[f]
                self.roll_str = roll = roll[len(f):]

        for o in valid_operators:
            if o in roll:
                self.operator = o
                roll, mod = roll.split(o)
                self.modifier = int(mod) * -1 if o == "-" else int(mod)

        self.number, self.sides = map(int, roll.split("d"))
        self.min_roll = self.number
        self.max_roll = self.sides * self.number

    def print_results(self, roll_result, name=None):
        """Return result of roll."""
        roll_plus_mods = "{} {} {}".format(
            roll_result,
            self.operator,
            abs(self.modifier)
        )

        final_result = "*[ {} ]* _({} = {}) (min {}, max {}) {}_".format(
            roll_result + self.modifier,
            self.roll_str,
            roll_plus_mods,
            self.min_roll + self.modifier,
            self.max_roll + self.modifier,
            self.message
        )

        if name:
            final_result += " with {}".format(name)
        return final_result

    def roll_die(self):
        """Standard roll of die."""
        import random
        result = 0
        for x in range(0, self.number):
            result += random.randint(1, self.sides)
        return result

    def advantage(self):
        """Roll with advantage."""
        self.message = "with advantage"
        return max(self.roll_die(), self.roll_die())

    def disadvantage(self):
        """Roll with disadvantage."""
        self.message = "with disadvantage"
        return min(self.roll_die(), self.roll_die())

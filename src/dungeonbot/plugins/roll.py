from dungeonbot.plugins.primordials import BangCommandPlugin
from dungeonbot.handlers.slack import SlackHandler

from dungeonbot.plugins.die_roll import DieRoll
from dungeonbot.models.roll import RollModel


class RollPlugin(BangCommandPlugin):
    """Plugin for roll."""

    help_text = """```
command:
    !roll

description:
    Rolls dice for you.

    This command is whitespace-agnostic.
    ("1d2+2" will be processed exactly the same as "1 d 2    +2")

    You can specify multiple die rolls in the same command as long as they
    are separated by commas.

    You can specify a roll to be made with advantage by prepending the roll
    with the `-a` flag (or just `a`), or with disadvantage by prepending the
    roll with `-d` (or just `d`).

    <PARAMS> are required
    [PARAMS] are optional


usage:
    !roll [ADVANTAGE/DISADVANTAGE] <HOW MANY> d <SIDES> [+/-MODIFIER] [, ... ]

examples:
    !roll 2d6
    !roll -d 1d20-2
    !roll a 1d20+4, 4d6, -d 1d20+3
```"""

    def run(self):
        """Run roll plugin."""
        bot = SlackHandler()

        args = self.arg_string.replace(" ", "").split(',')
        # user = bot.get_user_from_id(self.event['user'])

        message = "_*Roll result{} for {}:*_".format(
            "s" if len(args) > 1 else "",
            bot.get_user_from_id(self.event['user'])
        )

        for item in args:
            message += "\n" + self.process_roll(item)

        bot.make_post(self.event, message)

    def process_roll(self, roll_str):
        """Process Roll string."""
        # Save new Roll
        bot = SlackHandler()
        user = bot.get_user_from_id(self.event['user'])

        if roll_str.startswith("save"):
            parsed = RollModel.parse_key_val_pairs(roll_str.lstrip("save"))
            if parsed:
                instance = RollModel.new(parsed[0], parsed[1], user)
                return "Successfully Saved {}: {}".format(instance.key, instance.val)
            else:
                return "Not a valid Key/Value Pair"

        # list all saved rolls
        elif roll_str == "list":
            how_many = 10
            roll_str = roll_str.lstrip("list")
            if roll_str:
                how_many = int(roll_str)
            saved = RollModel.list(how_many=how_many, user=user)
            message = "*Saved Rolls for {}:*".format(user)
            for x in saved:
                message += "\n{}: {}".format(x.key, x.val)
            return message

        else:
            name = None
            saved_roll = RollModel.get_by_key(key=roll_str, user=user)
            if saved_roll:
                # if roll is saved, assign the saved rolls value to roll_str
                roll_str = saved_roll.val
                name = saved_roll.key

            # Create new roll object, and print result of obj's action.
            r = DieRoll(roll_str)
            return r.print_results(r.action(), name)

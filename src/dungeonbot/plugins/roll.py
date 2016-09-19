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
        """Run Roll Plugin."""
        bot = SlackHandler()

        user = bot.get_user_from_id(self.event['user'])
        args = self.arg_string.split(",")

        message = "_*Roll result{} for {}:*_".format(
            "s" if len(args) > 1 else "",
            user
        )

        for item in args:
            message += "\n" + self.process_roll(item, user)

        bot.make_post(self.event, message)

    def process_roll(self, user_input, user):
        """Parse user input and delegate to appropriate roll func."""
        args = user_input.split()

        commands = {
            "save": self.save_roll,
            "list": self.list_rolls,
            "delete": self.delete_roll,
        }

        if args[0] in commands:
            return commands[args[0]](args[1:], user)
        else:
            return self.make_roll(args, user)

    def save_roll(self, args, user):
        """Save new roll as key/val pair for requesting user."""
        key = args[0]
        val = "".join(args[1:])
        if not (key and val):
            return "Not a valid Key/Pair."
        instance = RollModel.new(key, val, user)
        return "Successfully Saved {}: {}".format(
            instance.key,
            instance.val
        )

    def delete_roll(self, args, user):
        """Delete existing roll via key."""
        key = "".join(args)
        instance = RollModel.get_by_key(key=key, user=user)
        if instance:
            return RollModel.delete(instance)
        else:
            return "Cannot find item {}".format(key)

    def list_rolls(self, args, user):
        """List requesting user's saved rolls.

        If additional argument is passed in, use as limit,
        otherwise limit to 10 results returned.
        """
        message = "*Saved Rolls for {}:*".format(user)

        how_many = int("".join(args)) if args else 10

        saved = RollModel.list(how_many=how_many, user=user)

        for x in saved:
            message += "\n{}: {}".format(x.key, x.val)
        return message

    def make_roll(self, args, user):
        """Roll given roll string and return result.

        If given roll string is existing saved string, look
        up entry and roll the associated value.
        """
        roll_flags = ["a", "d"]
        name = None

        if args[0].lstrip("-") in roll_flags:
            flag = args[0].lstrip("-")
            roll_str = "".join(args[1:])
        else:
            flag = None
            roll_str = "".join(args)

        saved_roll = RollModel.get_by_key(key=roll_str, user=user)

        if saved_roll:
            name = saved_roll.key
            roll_str = saved_roll.val.lstrip("-")
            if roll_str[0] in roll_flags:
                flag = roll_str[0]
                roll_str = roll_str[1:]

        r = DieRoll(roll_str, flag)
        return r.print_results(r.action(), name)

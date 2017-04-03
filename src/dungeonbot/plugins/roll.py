"""Define logic for the Roll plugin."""

from dungeonbot.plugins.primordials import BangCommandPlugin
from dungeonbot.handlers.slack import SlackHandler

from dungeonbot.plugins.helpers.die_roll import DieRoll
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

    You can also save a roll with a name, and then use that name later.

    <PARAMS> are required
    [PARAMS] are optional


usage:
    !roll [ADVANTAGE/DISADVANTAGE] <HOW MANY> d <SIDES> [+/-MODIFIER] [, ... ]
    !roll [SAVE/LIST/DELETE] <NAMED ROLL>
    !roll [ADVANTAGE/DISADVANTAGE] <NAMED ROLL>

examples:
    !roll 2d6
    !roll -d 1d20-2
    !roll a 1d20+4, 4d6, -d 1d20+3
    !roll save fireballdmg 8d6
    !roll fireballdmg
    !roll list
    !roll delete fireballdmg
```"""

    def run(self):
        """Run Roll Plugin."""
        bot = SlackHandler()

        user = bot.get_user_obj_from_id(self.event['user'])
        args = self.arg_string.split(",")

        message = "_*Roll result{} for {}:*_".format(
            "s" if len(args) > 1 else "",
            user["name"],
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

#        test = user_input.replace(" ", "").split("d")
#        if not test[0].isdigit() or not test[1].isdigit():
#            return "Not a valid command."
#        else:
#            return self.make_roll(args, user)

        # Shitty removal of validation, instead of a proper refactor
        # The issue is that the above block considers a roll with
        # advantage or disadvantage to be invalid
        #  - example: "-a 1d20" is invalid here
        return self.make_roll(args, user)

    def is_valid_roll_string(self, roll_str):
        """Check if roll string is valid, with or without a flag."""
        if not roll_str[0].isdigit():
            roll_str = roll_str[1:]
        return roll_str[0].isdigit() and roll_str[1] == "d" and roll_str[2].isdigit()

    def save_roll(self, args, user):
        """Save new roll as key/val pair for requesting user."""
        key = args[0]
        val = "".join(args[1:])
        if not (key and val):
            return "Not a valid Key/Pair."
        if not self.is_valid_roll_string(val):
            return "Not a properly formatted roll string."
        instance = RollModel.new(key=key, val=val, user=user)
        return "Successfully Saved " + instance.slack_msg

    def delete_roll(self, args, user):
        """Delete existing roll via key."""
        key = "".join(args)
        instance = RollModel.get(key=key, user=user)
        if instance:
            return "{} was successfully deleted.".format(RollModel.delete(instance))
        else:
            return "Cannot find item {}".format(key)

    def list_rolls(self, args, user):
        """List requesting user's saved rolls.

        If additional argument is passed in, use as limit,
        otherwise limit to 10 results returned.
        """
        message = "*Saved Rolls for {}:*".format(user["name"])

        how_many = int("".join(args)) if args else 10

        saved = RollModel.list(how_many=how_many, user=user)

        for x in saved:
            message += "\n" + x.slack_msg
        return message

    def parse_flag_and_roll_string(self, args):
        """Separate roll string and flag from args. Accepts a list and returns a string."""
        roll_flags = ["a", "d"]
        flag = None
        arg = args[0].lstrip("-")

        if arg[0] in roll_flags:
            flag = arg[0]
            roll_str = "".join(args[1:])
        else:
            roll_str = "".join(args)
        return roll_str, flag

    def make_roll(self, args, user):
        """Roll given roll string and return result.

        If given roll string is existing saved string, look
        up entry and roll the associated value.
        """
        name, temp_flag = None, None
        roll_str, flag = self.parse_flag_and_roll_string(args)
        saved_roll = RollModel.get(key=roll_str, user=user)

        if saved_roll:
            name = saved_roll.key
            roll_str, temp_flag = self.parse_flag_and_roll_string([saved_roll.val])
        r = DieRoll(roll_str, temp_flag or flag)
        return r.print_results(r.action(), name)

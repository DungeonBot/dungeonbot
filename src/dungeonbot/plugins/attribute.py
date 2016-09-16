from dungeonbot.plugins.primordials import BangCommandPlugin
from dungeonbot.handlers.slack import SlackHandler
from dungeonbot.models.attribute import AttrModel


class AttrPlugin(BangCommandPlugin):
    """Misc. key/value storage for player stats."""

    help_text = """
Command:
    !attr + ADDITIONAL COMMAND

Additional Commands:
    set
    get
    list
    delete KEY

Description:
    Stores Miscellaneous Key/Value pairs.
    Ideal for character statistics.

Examples:
    !attr set strength 14
    !attr get strength
    !attr list
    !attr delete strength
"""

    def run(self):
        bot = SlackHandler()
        user = bot.get_user_from_id(self.event["user"])

        args = self.arg_string.split()
        message = self.process_attr(args, user)
        bot.make_post(self.event, message)

    def process_attr(self, args, user):
        commands = {
            "get": AttrModel.get,
            "set": AttrModel.set,
            "list": AttrModel.list,
            "delete": AttrModel.delete,
        }

        command = args[0]
        args = args[1:]
        if command in commands:
            instance = commands[command](args=args, user=user)
            return self.print_result(instance, command)
        else:
            return "Not a valid command."


    def print_result(self, instance, command):
        message = "*Player Attributes:*"
        if type(instance) == str:
            message += "\n{} -- {}".format(command, instance)
        elif command == "list":
            message += "\n{}:".format(command)
            for i in instance:
                message += "\n{}: {}".format(i.key, i.val)
        elif instance:
            message += "\n{} -- {}: {}".format(command, instance.key, instance.val)
        else:
            message += "No Information on {} instance when running {}.".format(instance, command)
        return message


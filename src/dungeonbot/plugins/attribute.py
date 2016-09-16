from dungeonbot.plugins.primordials import BangCommandPlugin
from dungeonbot.handlers.slack import SlackHandler
from dungeonbot.models.attribute import AttrPlugin


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
        message = process_attr(args, user) 
        bot.make_post(self.event, message)

    def process_attr(self, args, user):
        commands = {
            "get": AttrPlugin.get,
            "set": AttrPlugin.set,
            "list": AttrPlugin.list,
            "delete": AttrPlugin.delete,
        }

        command = args[:1]
        args = args[1:]
        if command in commands:
            # instance = commands[command](args=args, user=user)
            # return self.print_result(instance)
            return commands[command](args=args, user=user)
        else:
            return "Not a valid command."


    def print_result(self, instance):
        pass



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
            "get": self.get_key,
            "set": self.set_key,
            "list": self.list_keys,
            "delete": self.delete_key,
        }

        command = args[0]
        args = args[1:]
        if command in commands:
            return commands[command](args=args, user=user)
        else:
            return "Not a valid command."

    def get_key(self, args, user):
        instance = AttrModel.get(args=args, user=user)
        if instance:
            message = "{}: {}".format(instance.key, instance.val)
        else:
            message = "Could not find {}".format(args)
        return message

    def set_key(self, args, user):
        instance = AttrModel.set(args=args, user=user)
        if instance == "duplicate":
            message = "You already have a key with that name."
        elif instance:
            message = "Saved:\n{}: {}".format(instance.key, instance.val)
        else:
            message = "Could not save key."
        return message

    def list_keys(self, args, user):
        instances = AttrModel.list(args=args, user=user)
        message = "Listing attributes for {}".format(user)
        for i in instances:
            message += "\n{}: {}".format(i.key, i.val)
        return message

    def delete_key(self, args, user):
        deleted_name = AttrModel.delete(args=args, user=user)
        if deleted_name:
            message = "Successfully deleted {}".format(deleted_name)
        else:
            message = "Could not delete key. "
        return message

from dungeonbot.plugins.primordials import BangCommandPlugin
from dungeonbot.handlers.slack import SlackHandler
from dungeonbot.models.highlights import HighlightModel


class HighlightPlugin(BangCommandPlugin):
    """Plugin for campaign Highlights."""

    help_text = """
    command:
        !log + ADDITIONAL COMMAND

    additional commands:
        add + TEXT
        list + [NUM]

    description:
        logs detailing game highlights.

        Can add a new entry with add, or list items already existing.
        List defaults to returning the 10 most recent entries, but
        the limit can be modified by passing in an optional number.

    examples:
        !log add some sweet thing that happened
        !log list 5
    """

    def run(self):
        """Run Highlight Plugin."""
        bot = SlackHandler()
        args = self.arg_string.split(" ", 1)
        message = self.process_highlight(args)
        bot.make_post(self.event, message)

    def process_highlight(self, args):
        """Process highlight command."""
        commands = {"add": self.add, "list": self.list_highlights}
        command = args[0]
        args = args[1:]
        if command not in commands:
            return """
                Whoops! That isn't a valid command.
                Maybe try !help log if you are stuck
            """
        return commands[command](args)

    def add(self, args):
        """Add new Highlight and return text."""
        instance = HighlightModel.new(args[0])
        message = "*New Campaign Highlight*\n{}".format(instance.text)
        return message

    def list_highlights(self, args):
        """List all existing campaign highlights.

        Defaults to listing last ten.
        """
        how_many = int(args[0]) if args else 10
        highlights = HighlightModel.list(how_many)
        message = "*{} Most Recent Campaign Highlights*".format(how_many)
        for h in highlights:
            message += "\n{}".format(h.text)
        return message

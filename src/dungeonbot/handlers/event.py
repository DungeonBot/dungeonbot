"""Define the EventHandler class."""

from dungeonbot.handlers.slack import SlackHandler
from dungeonbot.plugins import (
    help,
    karma,
    roll,
    quest,
    highlights
)


class EventHandler(object):
    """Parse events and call the appropriate plugin."""

    suffixes = ["++", "--"]

    def __init__(self, event):
        """Initialize EventHandler with an event passed in."""
        self.event = event

    def process_event(self):
        """Decide type of command.

        Commands can either be bang-commands or suffix-commands.

        """
        if self.event['text'][0] == "!":
            self.parse_bang_command()

        elif self.event['text'][-2:] in self.suffixes:
            self.parse_suffix_command()

    def parse_bang_command(self):
        """Parse a bang-command and call the appropriate plugin."""
        valid_commands = {
            'help': help.HelpPlugin,
            'karma': karma.KarmaPlugin,
            'karma_newest': karma.KarmaNewestPlugin,
            'karma_top': karma.KarmaTopPlugin,
            'karma_bottom': karma.KarmaBottomPlugin,
            'roll': roll.RollPlugin,
            'quest': quest.QuestPlugin,
            'log': highlights.HighlightPlugin
        }

        evt_string = self.event['text']
        cmd_string = evt_string[1:]

        try:
            command, arg_string = cmd_string.split(' ', 1)
        except ValueError:
            command, arg_string = cmd_string, ""

        if command in valid_commands:
            plugin = valid_commands[command](
                self.event,
                arg_string,
            )
            plugin.run()

        else:
            bot = SlackHandler()
            message = "Sorry, '!{}' is not a valid command.".format(command)
            bot.make_post(self.event, message)

    def parse_suffix_command(self):
        """Parse a suffix-command and call the appropriate plugin."""
        valid_suffixes = {
            '++': karma.KarmaModifyPlugin,
            '--': karma.KarmaModifyPlugin,
        }

        evt_string = self.event['text']

        arg_string, suffix = evt_string[:-2], evt_string[-2:]

        if arg_string and (suffix in valid_suffixes):
            plugin = valid_suffixes[suffix](
                self.event,
                arg_string,
                suffix
            )
            plugin.run()

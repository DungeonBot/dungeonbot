"""Define base plugins from which other plugins will inherit."""

from dungeonbot.handlers.slack import SlackHandler


class BasePlugin(object):
    """The root Plugin object.

    Provides all plugins with a default help method.

    """

    help_text = "Somebody didn't give their plugin any help text. For shame."

    def help(self):
        """Post help message to Slack."""
        bot = SlackHandler()
        bot.make_post(self.event, self.help_text)


class BangCommandPlugin(BasePlugin):
    """Base plugin for handling bang commands."""

    def __init__(self, event, arg_string):
        """Initialize plugin with event and arg string."""
        self.event = event
        self.arg_string = arg_string


class SuffixCommandPlugin(BasePlugin):
    """Base plugin for handling suffixed commands."""

    def __init__(self, event, arg_string, suffix=None):
        """Initialize plugin with event, arg string, and suffix."""
        self.event = event
        self.arg_string = arg_string
        self.suffix = suffix

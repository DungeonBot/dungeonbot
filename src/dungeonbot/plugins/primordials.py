"""Define base plugins from which other plugins will inherit."""

from dungeonbot.handlers.slack import SlackHandler


class BasePlugin(object):
    """The root Plugin object.

    Provides all plugins with a default help text.

    """

    help_text = "Somebody didn't give their plugin any help text. For shame."


class SlackEnabledPlugin(BasePlugin):
    """Base plugin equipped with a SlackHandler.

    Provides all plugins with `self.bot` and a help method.

    """

    def __init__(self, event):
        """Setup plugin with SlackHandler and event."""
        self.bot = SlackHandler()
        self.event = event

    def help(self):
        """Post help message to Slack."""
        self.bot.make_post(self.event, self.help_text)


class BangCommandPlugin(SlackEnabledPlugin):
    """Base plugin for handling bang commands."""

    def __init__(self, event, arg_string):
        """Initialize plugin with event and arg string."""
        super().__init__(event)

        self.arg_string = arg_string


class SuffixCommandPlugin(SlackEnabledPlugin):
    """Base plugin for handling suffixed commands."""

    def __init__(self, event, arg_string, suffix=None):
        """Initialize plugin with event, arg string, and suffix."""
        super().__init__(event)
        self.arg_string = arg_string
        self.suffix = suffix

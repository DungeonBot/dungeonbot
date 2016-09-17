from dungeonbot.plugins.primordials import BangCommandPlugin
from dungeonbot.handlers.slack import SlackHandler
from dungeonbot.models.highlights import HighlightModel


class HighlightPlugin(BangCommandPlugin):
    """Plugin for campaign Highlights."""

    help_text = """"""

    def run(self):
        """Run Highlight Plugin."""
        bot = SlackHandler()
        message = "something."
        bot.make_post(self.event, message)

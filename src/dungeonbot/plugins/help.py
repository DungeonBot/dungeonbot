"""Define logic for the Help plugin."""

from dungeonbot.plugins.primordials import BangCommandPlugin
from dungeonbot.plugins.karma import (
    KarmaPlugin,
    KarmaNewestPlugin,
    KarmaTopPlugin,
    KarmaBottomPlugin,
)
from dungeonbot.plugins.roll import RollPlugin
from dungeonbot.plugins.quest import QuestPlugin
from dungeonbot.plugins.highlights import HighlightPlugin
from dungeonbot.plugins.attribute import AttrPlugin


class HelpPlugin(BangCommandPlugin):
    """Switchboard for `!help` commands."""

    help_topics = {
        'karma': KarmaPlugin,
        'karma_newest': KarmaNewestPlugin,
        'karma_top': KarmaTopPlugin,
        'karma_bottom': KarmaBottomPlugin,
        'roll': RollPlugin,
        'quest': QuestPlugin,
        'log': HighlightPlugin,
        'attr': AttrPlugin,
    }

    help_text = """```
available help topics:
    help
    karma
    roll
    quest
    attr

Try `!help [topic]` for information on a specific topic.
```"""

    def run(self):
        """Run the `help()` function of the appropriate plugin."""
        args = self.arg_string.split()

        if args and args[0] in self.help_topics:
            plugin = self.help_topics[args[0]](self.event, self.arg_string)
            plugin.help()

        else:
            self.help()

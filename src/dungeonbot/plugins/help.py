"""Define logic for the Help plugin."""

from dungeonbot.plugins.primordials import BangCommandPlugin
from dungeonbot.plugins.attribute import AttrPlugin
from dungeonbot.plugins.highlights import HighlightPlugin
from dungeonbot.plugins.initiative import InitiativePlugin
from dungeonbot.plugins.karma import (
    KarmaPlugin,
    KarmaNewestPlugin,
    KarmaTopPlugin,
    KarmaBottomPlugin,
)
from dungeonbot.plugins.quest import QuestPlugin
from dungeonbot.plugins.roll import RollPlugin


class HelpPlugin(BangCommandPlugin):
    """Switchboard for `!help` commands."""

    help_topics = {
        'attr': AttrPlugin,
        'init': InitiativePlugin,
        'karma': KarmaPlugin,
        'karma_newest': KarmaNewestPlugin,
        'karma_top': KarmaTopPlugin,
        'karma_bottom': KarmaBottomPlugin,
        'log': HighlightPlugin,
        'quest': QuestPlugin,
        'roll': RollPlugin,
    }

    help_text = """```
available help topics:
    attr
    help
    init
    karma
    quest
    roll

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

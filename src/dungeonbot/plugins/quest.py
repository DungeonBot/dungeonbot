from dungeonbot.plugins.primordials import (
    BangCommandPlugin,
)
from dungeonbot.handlers.slack import SlackHandler
from dungeonbot.models import QuestModel


class QuestPlugin(BangCommandPlugin):
    help_text = '\n'.join([
        "```",
        "command:",
        "    !quest",
        "",
        "description:",
        "    Keeps track of our quests.",
        "",
        "usage:",
        "    !quest log [INTEGER]",
        "",
        "    (<PARAMS> are required",
        "    [PARAMS] are optional)",
        "",
        "examples:",
        "    !quest log",
        "    !quest log 3",
        "```",
    ])

    def run(self):
        """
        Handle valid sub-commands and return whatever view of quests we want.
        """

        bot = SlackHandler()
        args = self.arg_string.split(" ")

        valid_subcommands = {
            "log": self.list_active,
            "new": self.add_new,
            "edit": self.edit_quest,
            "detail": self.get_detail,
            "update": self.update_quest,
            "complete": self.complete_quest,
        }

        if args[0] not in valid_subcommands.keys():
            message = self.invalid_input()

        else:
            message = valid_subcommands[args[0]](*args)

        bot.make_post(self.event, message)

    def list_active(self, *args):
        """List N active quests. If none are active, say so."""

        try:
            quests = QuestModel.list_active(int(args[1]))
        except ValueError, IndexError:
            quests = QuestModel.list_active()

        if quests:
            message = ["ID    Date Added    Title"]
            for quest in quests:
                message.append("{}   {}   {}".format(quest.id,
                                                     quest.created.strftime(
                                                         "%b %d, %Y %H:%M"),
                                                     quest.title))

        else:
            message = [
                "```",
                "Currently there aren't any active quests for your party.",
                "",
                'Use "!quest new" to add new quests to the log!',
                "```"
            ]

        return "\n".join(message)

    def add_new(self, *args):
        """Add a new quest to the quest log."""
        return "Not yet implemented."

    def get_detail(self, *args):
        """Get the information for a single quest given its ID."""
        return "Not yet implemented."

    def edit_quest(self, *args):
        """Edit a particular field or fields for a quest."""
        return "Not yet implemented."

    def update_quest(self, *args):
        """Update the quest detail."""
        return "Not yet implemented."

    def complete_quest(self, *args):
        """Finish the quest and change its status to inactive."""
        return "Not yet implemented."

    def invalid_input(self):
        """Notify that the supplied subcommand is invalid"""
        return 'Please use a valid argument. "!help quest" for a list of valid arguments.'

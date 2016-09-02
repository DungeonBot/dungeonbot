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
        "    !quest log [PARAMS]",
        "",
        "    (<PARAMS> are required",
        "    [PARAMS] are optional)",
        "",
        "examples:",
        "    !quest log",
        "```",
    ])

    def run(self):
        """
        List the quests in the order which they were created.
        """

        bot = SlackHandler()

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
                'Use "!quest add" to add new quests to the log!',
                "```"
            ]

        message = "\n".join(message)
        bot.make_post(self.event, message)

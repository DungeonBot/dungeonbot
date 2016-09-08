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
        "    !quest new <CASE INSENSITIVE STRING>",
        "    !quest detail [INTEGER]",
        "    !quest detail <CASE INSENSITIVE STRING>",
        "",
        "    (<PARAMS> are required",
        "    [PARAMS] are optional)",
        "",
        "examples:",
        "    !quest log",
        "    !quest log 3",
        "    !quest new Kill the Grue.",
        "    !quest detail 1",
        "    !quest detail Kill the Grue.",
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
        except (ValueError, IndexError):
            quests = QuestModel.list_active()

        if quests and isinstance(quests, list):
            message = [
                "ID\tDate Added\t\tTitle",
                "--------------------------------------------------------------",
            ]
            for quest in quests:
                message.append("{}\t{}\t{}".format(quest.id,
                                                   quest.created.strftime(
                                                       "%b %d, %Y %H:%M"),
                                                   quest.title.capitalize()))

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
        args = " ".join(args)
        title = " ".join(args.split(" ", 1)[1:])

        if title:
            new_quest = QuestModel.new(title=title.lower())
            return "Added Quest #{}: {}".format(new_quest.id, new_quest.title)
        return "You must supply a title to add a quest."

    def get_detail(self, *args):
        """Get the information for a single quest given its title or ID."""
        try:
            the_id = int(args[1])
            quest = QuestModel.get_by_id(the_id)

        except ValueError:
            the_title = " ".join(args[1:]).lower()
            quest = QuestModel.get_by_name(the_title)

        except IndexError:
            return 'You should supply either a quest title or a quest ID. "!help quest" for examples on usage.'

        if quest:
            return self._slack_msg(quest)

        else:
            return 'Quest not found. "!quest log" for a list of active quests.'

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

    def _slack_msg(self, quest):

        # import pdb; pdb.set_trace()

        output = [
            "```",
            "*Quest #{}: {}*".format(quest.id, quest.title.title()),
            "-----------------------",
        ]
        if quest.description:
            output.append("{}\n\n".format("\n".join(quest.description.split("||"))))
        if quest.quest_giver:
            output.append("_Given by {}_".format(quest.quest_giver))
        if quest.location_given:
            output.append("_Given in {}_".format(quest.location_given))
        output.append("_Date Added: {}_".format(quest.created.strftime("%b %d, %Y %H:%M")))
        output.append("_Last Updated: {}_".format(quest.last_updated.strftime("%b %d, %Y %H:%M")))
        if quest.status:
            output.append("Status: Active")
        else:
            output.append("Status: Inactive | Completed: {}".format(quest.completed_date.strftime("%b %d, %Y %H:%M")))

        output.append("```")
        output = "\n".join(output)
        return output

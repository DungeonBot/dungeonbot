from dungeonbot.handlers.slack import SlackHandler
from dungeonbot.models.quest import QuestModel
from dungeonbot.plugins.primordials import BangCommandPlugin

TIME_FMT = "%b %d, %Y %H:%M"


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
        "    !quest detail <INTEGER>",
        "    !quest detail <CASE INSENSITIVE STRING>",
        "    !quest edit <INTEGER> <title|description|quest_giver|location> [CASE SENSITIVE STRING]",
        "    !quest update <INTEGER> <CASE SENSITIVE STRING>",
        "    !quest complete <INTEGER>",
        "    !quest complete <CASE INSENSITIVE STRING>",
        "",
        "    (<PARAMS> are required",
        "    [PARAMS] are optional)",
        "",
        "examples:",
        "    !quest log",
        "    !quest log 3",
        "    !quest new Kill the Grue",
        "    !quest detail 1",
        "    !quest detail Kill the Grue",
        "    !quest edit 1 title Kill all the Grues",
        "    !quest edit 1 description We've gotta go and murder everything.",
        "    !quest edit 1 quest_giver Flerg the Blerg",
        "    !quest edit 1 location Phandolin",
        "    !quest update 1 Words that will add to the description and not replace it.",
        "    !quest complete 1",
        "    !quest complete Kill the Grue",
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
            message = self._invalid_input()

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
                "ID\tDate Added\t\t\tTitle",
                "------------------------------------------------------------",
            ]
            for quest in quests:
                message.append("{}\t{}\t{}".format(quest.id,
                                                   quest.created.strftime(TIME_FMT),
                                                   quest.title.title()))

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
            quest = self._get_id_or_name(args)

        except IndexError:
            return 'You should supply either a quest title or a quest ID. "!help quest" for examples on usage.'

        if quest:
            return self._slack_msg(quest)

        return self._not_found()

    def update_quest(self, *args):
        """Update the quest detail."""
        try:
            quest_id = int(args[1])
            quest = QuestModel.get_by_id(quest_id)

        except ValueError:
            return 'You need to supply a quest ID. "!help quest" for examples on usage.'

        if quest:
            desc = " ".join(args[2:])

            if desc:
                QuestModel.add_detail(quest_id, desc)
                output = "*{}* description updated.".format(quest.title.title())
                output += "\n\n-----------------------\n\n"
                output += self._slack_msg(quest)
                return output

            else:
                return "You need to supply a description of some sort."

        return self._not_found()

    def complete_quest(self, *args):
        """Finish the quest and change its status to inactive."""
        try:
            quest = self._get_id_or_name(args)

        except IndexError:
            return 'You should supply either a quest title or a quest ID. "!help quest" for examples on usage.'

        if quest and quest.status:
            QuestModel.complete(quest.id)
            return "Congratulations on completing {}!".format(quest.title.title())

        elif quest and not quest.status:
            return "This quest has already been completed!"

        return self._not_found()

    def edit_quest(self, *args):
        """Edit a particular field or fields for a quest."""
        try:
            quest_id = int(args[1])
            quest = QuestModel.get_by_id(quest_id)

        except ValueError:
            return 'You need to supply a quest ID. "!help quest" for examples on usage.'

        if quest:
            try:
                this_field = args[2].lower()

            except IndexError:
                return 'You need to supply a field to be edited: [title|description|quest_giver|location]'

            white_list = ["title", "description", "quest_giver", "location"]

            if this_field not in white_list:
                return 'That is not a field you can edit. Try again: [title|description|quest_giver|location]'

            new_val = " ".join(args[3:]).strip()

            if not new_val:
                return 'You must provide a value for the "{}" field.'.format(this_field)

            inputs = {this_field: new_val}
            QuestModel.modify(quest.id, **inputs)

            output = "*{}* {} edited.".format(quest.title.title(), this_field)
            output += "\n\n-----------------------\n\n"
            output += self._slack_msg(quest)
            return output

        return self._not_found()

    def _invalid_input(self):
        """Notify that the supplied subcommand is invalid."""
        return 'Please use a valid argument. "!help quest" for a list of valid arguments.'

    def _not_found(self):
        """Notify that the supplied quest id or name doesn't exist"""
        return 'Quest not found. "!quest log" for a list of active quests.'

    def _get_id_or_name(self, args):
        """Use the quest ID or quest name to retrieve from the database."""

        try:
            the_id = int(args[1])
            quest = QuestModel.get_by_id(the_id)

        except ValueError:
            the_title = " ".join(args[1:]).lower()
            quest = QuestModel.get_by_name(the_title)

        return quest

    def _slack_msg(self, quest):
        """Return detail about an individual quest."""

        output = [
            "```",
            "*Quest #{}: {}*".format(quest.id, quest.title.title()),
            "-----------------------",
        ]
        if quest.description:
            output.append("{}\n\n".format("\n\n".join(quest.description.split("||"))))

        if quest.quest_giver:
            output.append("_Given by {}_".format(quest.quest_giver))

        if quest.location_given:
            output.append("_Given in {}_".format(quest.location_given))

        output.append("_Date Added: {}_".format(quest.created.strftime(TIME_FMT)))
        output.append("_Last Updated: {}_".format(quest.last_updated.strftime(TIME_FMT)))

        if quest.status:
            output.append("Status: Active")
        else:
            output.append("Status: Inactive | Completed: {}".format(quest.completed_date.strftime(TIME_FMT)))

        output.append("```")
        output = "\n".join(output)
        return output

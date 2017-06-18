from dungeonbot.plugins.primordials import BangCommandPlugin
from dungeonbot.handlers.slack import SlackHandler
from dungeonbot.models.initiative import InitiativeModel

from random import randint


class InitiativePlugin(BangCommandPlugin):
    """Initiative tracker."""

    help_text = """```
Command:
    !init + SUBCOMMAND

Subcommands:
    get NAME (, NAME, ...)
    add NAME [ INITIATIVE | -r MODIFIER ] (, NAME [ INITIATIVE | -r MODIFIER], ...)
    remove NAME (, NAME, ...)
    list
    clear

Description:
    Manages entities in an initiative order.

    New entities can be added by either specifying an initiative value,
    or by passing the '-r' flag and a modifier to have DungeonBot roll
    the initiative for you (if the '-r' flag is present but no modifier
    is supplied, DungeonBot will roll a straight d20).

    The 'get', 'add', and 'remove' subcommands can all specify a single
    entity or a comma-separated list of entities.

Examples:
    !init add Beholder 16
    !init add Minsk -r +3, Boo -r +7
    !init get Boo
    !init remove Minsk
    !init remove Boo, Beholder
    !init list
    !init clear
```"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = SlackHandler()

    def run(self):
        """Run Initiative plugin."""
        bot = self.bot
        subcommands = {
            "get": self.get_entity,
            "add": self.add_entity,
            "remove": self.remove_entity,
            "list": self.list_initiative,
            "clear": self.clear_initiative,
        }
        
        subcommand, *args = self.arg_string.split(None, 1)
        args = args[0] if args else None
        if subcommand in subcommands:
            message = subcommands[subcommand](args=args)
        else:
            message = f"'{subcommand}': Not a valid !init subcommand."

        bot.make_post(self.event, message)
    
    def get_entity(self, args):
        """Get initiative value(s) for an entity (or several comma-separated entities)."""
        entities = []
        for name in args.split(','):
            name = name.strip()
            instance = InitiativeModel.get(name=name)
            entities.append((name, instance.init if instance else None))
        
        message = "*Initiative Query Results:*"
        for pair in entities:
            message += f"\n{pair[0]}: {pair[1]}" if pair[1] else f"\n{pair[0]}: Not Found"

        return message

    def add_entity(self, args):
        """Add an entity (or several comma-separated entities) to the initiative list.

        Valid entity formats:
            NAME VALUE
            NAME -r MODIFIER
            NAME -r
        """
        errors = ""
        for entity in args.split(","):
            entity = entity.strip()
            # '-r' flag supplied with trailing modifier:
            if " -r " in entity:
                name, _, modifier = entity.rsplit(None, 2)
                try:
                    modifier = int(modifier)
                except ValueError:
                    errors += f"\n'{entity}': Modifier must be a positive or negative integer."
                    continue

                instance = InitiativeModel.set(name=name, init=randint(1, 20) + modifier)
                if instance == "duplicate":
                    errors += f"\n'{entity}': Duplicate entity name."
                    continue

            # '-r' flag supplied, but no modifier:
            elif " -r" in entity:
                name, _ = entity.rsplit(None, 1)
                instance = InitiativeModel.set(name=name, init=randint(1, 20))
                if instance == "duplicate":
                    errors += f"\n'{entity}': Duplicate entity name."
                    continue

            # no 'r' flag:
            else:
                name, *init = entity.rsplit(None, 1)
                init = init[0] if init else None
                try:
                    init = int(init)
                except (ValueError, TypeError):
                    errors += f"\n'{entity}': Value not given or not an integer."
                    continue

                instance = InitiativeModel.set(name=name, init=init)
                if instance == "duplicate":
                    errors += f"\n'{entity}': Duplicate entity name."

        if errors:
            return f"Errors:{errors}\n\nOther entries not mentioned should have worked."

        return "Entity (or entities) added."


    def remove_entity(self, args):
        """Remove an entity (or several comma-separated entities) from the initiative list."""
        for name in args.split(","):
            name = name.strip()
            InitiativeModel.delete(name=name)

        return "Done."

    def list_initiative(self, args=None):
        """List the current initiative list in descending order.
        
        This command takes no [args], and they will be ignored if supplied.
        """
        message = "*Current Initiative:*"
        entities = InitiativeModel.list()
        for entity in entities:
            message += f"\n> _*{entity.init}*_ -- {entity.name}"

        return message

    def clear_initiative(self, args=None):
        """Remove all entites in the initiative list.

        This command takes no [args], and they will be ignored if supplied.
        """
        InitiativeModel.clear()
        return "Initiative cleared."


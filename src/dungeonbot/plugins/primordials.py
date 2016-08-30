from dungeonbot import handlers


class BasePlugin(object):
    help_text = "Somebody didn't give their plugin any help text. For shame."

    def help(self):
        bot = handlers.SlackHandler()
        bot.make_post(self.event, self.help_text)


class BangCommandPlugin(BasePlugin):
    def __init__(self, event, arg_string):
        self.event = event
        self.arg_string = arg_string


class HybridCommandPlugin(BasePlugin):
    def __init__(self, event, arg_string, suffix=None):
        self.event = event
        self.arg_string = arg_string
        self.suffix = suffix

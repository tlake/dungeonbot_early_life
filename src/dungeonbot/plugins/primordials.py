from dungeonbot.handlers.slack import SlackHandler


class BasePlugin(object):
    help_text = "Somebody didn't give their plugin any help text. For shame."

    def help(self):
        bot = SlackHandler()
        bot.make_post(self.event, self.help_text)


class BangCommandPlugin(BasePlugin):
    def __init__(self, event, arg_string):
        self.event = event
        self.arg_string = arg_string


class SuffixCommandPlugin(BasePlugin):
    def __init__(self, event, arg_string, suffix=None):
        self.event = event
        self.arg_string = arg_string
        self.suffix = suffix

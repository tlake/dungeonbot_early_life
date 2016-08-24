from slacker import Slacker
import plugins
import os


class SlackHandler(object):
    def __init__(self):
        self.slack = Slacker(os.getenv("BOT_ACCESS_TOKEN"))

    def make_post(self, event, message):
        self.slack.chat.post_message(
            event['channel'],
            message,
            as_user=True,
        )

    def get_user_from_id(self, user_id):
        member_entry = [x for x in self.slack.users.list().body['members'] if user_id in x["id"]][0]
        return member_entry["name"]


class EventHandler(object):

    valid_commands = {
        'help': plugins.HelpPlugin,
        'roll': plugins.RollPlugin,
    }

    def __init__(self, event):
        self.event = event
        try:
            self.command, self.arg_string = event['text'].split(' ', 1)
        except ValueError:
            self.command, self.arg_string = event['text'], ""

    def parse_command(self):
        if self.command in self.valid_commands:
            plugin = self.valid_commands[self.command](
                self.event,
                self.arg_string
            )
            plugin.run()

        else:
            bot = SlackHandler()
            message = "Sorry, {} is not a valid command.".format(self.command)
            bot.make_post(self.event, message)

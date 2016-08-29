
class SlackHandler(object):
    def __init__(self):
        from slacker import Slacker
        import os

        self.slack = Slacker(os.environ.get("BOT_ACCESS_TOKEN"))

    def make_post(self, event, message):
        import os

        if os.getenv("PERMISSION_TO_SPEAK"):
            self.slack.chat.post_message(
                event['channel'],
                message,
                as_user=True,
            )

        else:
            from auxiliaries.helpers import eprint
            message = '\n\n' + message + '\n'
            eprint("Message that would have been sent to Slack:", message)

    def get_user_from_id(self, user_id):
        import os

        if os.getenv("PERMISSION_TO_SPEAK"):
            member_entry = [x for x in self.slack.users.list().body['members'] if user_id in x["id"]][0]
            return member_entry["name"]
        else:
            return "USERNAME"


class EventHandler(object):
    from dungeonbot import plugins

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

import os
from slacker import Slacker
from dungeonbot import plugins
from auxiliaries.helpers import eprint


class SlackHandler(object):
    def __init__(self):
        # from slacker import Slacker
        # import os

        self.slack = Slacker(os.environ.get("BOT_ACCESS_TOKEN"))

    def make_post(self, event, message):
        # import os

        if os.getenv("PERMISSION_TO_SPEAK"):
            self.slack.chat.post_message(
                event['channel'],
                message,
                as_user=True,
            )

        else:
            # from auxiliaries.helpers import eprint
            message = '\n\n' + message + '\n'
            eprint("Message that would have been sent to Slack:", message)

    def get_user_obj_from_id(self, user_id):
        if os.getenv("PERMISSION_TO_SPEAK"):
            members_dict = self.slack.users.list().body['members']
            for entry in members_dict:
                if user_id in entry['id']:
                    return entry
            # return [x for x in self.slack.users.list().body['members']
            # if user_id in x["id"]][0]

    def get_user_from_id(self, user_id):
        # import os

        if os.getenv("PERMISSION_TO_SPEAK"):
            user_obj = self.get_user_obj_from_id(user_id)
            return user_obj['name']
        else:
            return "USERNAME"

    def get_userid_from_name(self, username):
        if os.getenv("PERMISSION_TO_SPEAK"):
            return self.slack.users.get_user_id(username)
        else:
            return "USERID_012345"


class EventHandler(object):
    # from dungeonbot import plugins
    suffixes = ["++", "--"]

    def __init__(self, event):
        self.event = event

    def process_event(self):
        # event is a '!' command
        if self.event['text'][0] == "!":
            self.parse_bang_command()

        # event is a suffix command
        elif self.event['text'][-2:] in self.suffixes:
            self.parse_suffix_command()

    def parse_bang_command(self):
        valid_commands = {
            'help': plugins.HelpPlugin,
            'roll': plugins.RollPlugin,
            'karma': plugins.KarmaPlugin,
        }

        evt_string = self.event['text']
        cmd_string = evt_string[1:]

        try:
            command, arg_string = cmd_string.split(' ', 1)
        except ValueError:
            command, arg_string = cmd_string, ""

        if command in valid_commands:
            plugin = valid_commands[command](
                self.event,
                arg_string
            )
            plugin.run()

        else:
            bot = SlackHandler()
            message = "Sorry,'!{}' is not a valid command.".format(command)
            bot.make_post(self.event, message)

    def parse_suffix_command(self):
        valid_suffixes = {
            '++': plugins.KarmaPlugin,
            '--': plugins.KarmaPlugin,
        }

        evt_string = self.event['text']

        arg_string, suffix = evt_string[:-2], evt_string[-2:]

        if arg_string and (suffix in valid_suffixes):
            plugin = valid_suffixes[suffix](
                self.event,
                arg_string,
                suffix
            )
            plugin.run()

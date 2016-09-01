import os
from slacker import Slacker
from dungeonbot.plugins import (
    help,
    karma,
    roll,
)
from auxiliaries.helpers import eprint


class SlackHandler(object):
    def __init__(self):
        self.slack = Slacker(os.environ.get("BOT_ACCESS_TOKEN"))

    def make_post(self, event, message):
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
        else:
            return {
                'color': '99a949',
                'deleted': False,
                'id': 'SLACK_USERID',
                'is_admin': False,
                'is_bot': True,
                'is_owner': False,
                'is_primary_owner': False,
                'is_restricted': False,
                'is_ultra_restricted': False,
                'name': 'example_dungeonbot',
                'profile': {
                    'api_app_id': '',
                    'avatar_hash': 'some_hash',
                    'bot_id': 'SLACK_BOT_ID',
                    'first_name': 'Dungeon',
                    'image_1024': 'https://img_url.png',
                    'image_192': 'https://img_url.png',
                    'image_24': 'https://img_url.png',
                    'image_32': 'https://img_url.png',
                    'image_48': 'https://img_url.png',
                    'image_512': 'https://img_url.png',
                    'image_72': 'https://img_url.png',
                    'image_original': 'https://img_url.png',
                    'last_name': 'Bot',
                    'real_name': 'Dungeon Bot',
                    'real_name_normalized': 'Dungeon Bot'
                },
                'real_name': 'Dungeon Bot',
                'status': None,
                'team_id': 'SLACK_TEAM_ID',
                'tz': None,
                'tz_label': 'Pacific Daylight Time',
                'tz_offset': -25200
            }

    def get_user_from_id(self, user_id):
        if os.getenv("PERMISSION_TO_SPEAK"):
            user_obj = self.get_user_obj_from_id(user_id)
            return user_obj['name']
        else:
            return "A_SLACK_USERNAME"

    def get_userid_from_name(self, username):
        if os.getenv("PERMISSION_TO_SPEAK"):
            return self.slack.users.get_user_id(username)
        else:
            return "A_SLACK_USERID"


class EventHandler(object):
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
            'help': help.HelpPlugin,
            'karma': karma.KarmaPlugin,
            'karma_newest': karma.KarmaNewestPlugin,
            'karma_top': karma.KarmaTopPlugin,
            'karma_bottom': karma.KarmaBottomPlugin,
            'roll': roll.RollPlugin,
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
                arg_string,
            )
            plugin.run()

        else:
            bot = SlackHandler()
            message = "Sorry,'!{}' is not a valid command.".format(command)
            bot.make_post(self.event, message)

    def parse_suffix_command(self):
        valid_suffixes = {
            '++': karma.KarmaModifyPlugin,
            '--': karma.KarmaModifyPlugin,
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

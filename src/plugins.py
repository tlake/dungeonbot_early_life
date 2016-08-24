import handlers

import random


class Plugin(object):
    def __init__(self, event, arg_string):
        self.event = event
        self.arg_string = arg_string


class RollPlugin(Plugin):
    def help(self):
        bot = handlers.SlackHandler()
        help_text = """```
command:
    !roll

description:
    Rolls dice for you.

usage:
    !roll [NUMBER OF DICE]d[DIE SIDES][+/-MODIFIER]

examples:
    !roll 2d6
    !roll 1d20+4
```"""

        bot.make_post(self.event, help_text)

    def run(self):
        bot = handlers.SlackHandler()
        args = self.arg_string.replace(" ", "")
        roll = ""
        operator = "+"
        modifier = 0

        if "+" in args:
            roll, modifier = args.split("+")
        elif "-" in args:
            operator = "-"
            roll, modifier = args.split("-")
        else:
            roll = args

        number, sides = roll.split("d")
        modifier = int(modifier)
        number = int(number)
        sides = int(sides)
        roll_result = 0
        for x in range(0, number):
            roll_result += random.randint(1, sides)
        roll_plus_mods = "{} {} {}".format(
                str(roll_result),
                operator,
                str(modifier)
        )

        result = roll_result + modifier if operator == "+" else roll_result - modifier

        event_user_id = self.event['user']
        event_user_name = bot.get_user_from_id(event_user_id)

        final_result = "*{} rolls a {}* _({} = {})_".format(
                event_user_name,
                result,
                args,
                roll_plus_mods
            )

        bot.make_post(self.event, final_result)


class HelpPlugin(Plugin):
    help_topics = {
        'roll': RollPlugin,
    }

    help_text = """```
available commands:
    help
    roll

Try `!help [command]` for information on a specific command.
```"""

    def run(self):
        args = self.arg_string.split()

        if args and args[0] in self.help_topics:
            plugin = self.help_topics[args[0]](self.event, self.arg_string)
            plugin.help()

        else:
            bot = handlers.SlackHandler()
            message = self.help_text
            bot.make_post(self.event, message)

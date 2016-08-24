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
    !roll [NUMBER OF DICE]d[DIE SIDES][+/-MODIFIER] and [NUMBER OF DICE]d[DIE SIDES][+/-MODIFIER] and ...

examples:
    !roll 2d6
    !roll 1d20+4
    !roll 1d6 and 1d4+2 and 2d8-1
```"""

        bot.make_post(self.event, help_text)

    def run(self):
        bot = handlers.SlackHandler()
        args = self.arg_string.replace(" ", "")

        if len(args.split('and')) > 1:
            all_rolls = [' '.join(self._roll_func(bot, this_roll).split(' ')[1:]) for this_roll in args.split('and')]
            final_result = '*' + bot.get_user_from_id(self.event['user']) + '* ' + '\n\t and '.join(all_rolls)

        else:
            final_result = self._roll_func(bot, args)

        bot.make_post(self.event, final_result)


    def _roll_func(self, bot, roll_str):
        roll = ""
        operator = "+"
        modifier = 0

        if "+" in roll_str:
            roll, modifier = roll_str.split("+")
        elif "-" in roll_str:
            operator = "-"
            roll, modifier = roll_str.split("-")
        else:
            roll = roll_str

        number, sides = roll.split("d")
        modifier = int(modifier)
        number = int(number)
        sides = int(sides)
        roll_result = 0
        min_roll = 0
        max_roll = 0

        for x in range(0, number):
            roll_result += random.randint(1, sides)
            min_roll += 1
            max_roll += sides

        roll_plus_mods = "{} {} {}".format(
                str(roll_result),
                operator,
                str(modifier)
        )

        mod_result = modifier if operator == "+" else modifier * -1
        # result = roll_result + modifier if operator == "+" else roll_result - modifier
        result = roll_result + mod_result

        event_user_id = self.event['user']
        event_user_name = bot.get_user_from_id(event_user_id)

        final_result = "*{}* *rolls a {}* _({} = {})_ _(min: {}, max: {})_".format(
                event_user_name,
                result,
                roll_str,
                roll_plus_mods,
                min_roll + mod_result,
                max_roll + mod_result
            )
        return final_result



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

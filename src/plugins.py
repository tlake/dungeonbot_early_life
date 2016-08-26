
class Plugin(object):
    help_text = "No help exists for this plugin."

    def __init__(self, event, arg_string):
        self.event = event
        self.arg_string = arg_string

    def help(self):
        import handlers
        bot = handlers.SlackHandler()
        bot.make_post(self.event, self.help_text)


class RollPlugin(Plugin):
    help_text = """```
command:
    !roll

description:
    Rolls dice for you.

usage:
    !roll [HOW MANY]d[SIDES][+/-MODIFIER]
    !roll [HOW MANY]d[SIDES][+/-MODIFIER], [HOW MANY]d[SIDES][+/-MODIFIER], ...

examples:
    !roll 2d6
    !roll 1d20+4
    !roll 1d6, 1d4+2, 2d8-1
```"""

    def run(self):
        import handlers
        bot = handlers.SlackHandler()

        args = self.arg_string.replace(" ", "").split(',')

        message = "_*Roll result{} for {}:*_".format(
            "s" if len(args) > 1 else "",
            bot.get_user_from_id(self.event['user'])
        )

        for item in args:
            message += "\n" + self.process_roll(item)

        bot.make_post(self.event, message)

    def process_roll(self, roll_str):
        import random

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
        result = roll_result + mod_result

        final_result = "*[ {} ]* _({} = {}) (min {}, max {})_".format(
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
available help topics:
    help
    roll

Try `!help [topic]` for information on a specific topic.
```"""

    def run(self):
        args = self.arg_string.split()

        if args and args[0] in self.help_topics:
            plugin = self.help_topics[args[0]](self.event, self.arg_string)
            plugin.help()

        else:
            self.help()

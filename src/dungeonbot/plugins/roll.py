from dungeonbot.plugins.primordials import BangCommandPlugin
from dungeonbot.handlers.slack import SlackHandler

import random


class RollPlugin(BangCommandPlugin):
    help_text = """```
command:
    !roll

description:
    Rolls dice for you.

    This command is whitespace-agnostic.
    ("1d2+2" will be processed exactly the same as "1 d 2    +2")

    You can specify multiple die rolls in the same command as long as they
    are separated by commas.

    You can specify a roll to be made with advantage by prepending the roll
    with the `-a` flag (or just `a`), or with disadvantage by prepending the
    roll with `-d` (or just `d`).

    <PARAMS> are required
    [PARAMS] are optional


usage:
    !roll [ADVANTAGE/DISADVANTAGE] <HOW MANY> d <SIDES> [+/-MODIFIER] [, ... ]

examples:
    !roll 2d6
    !roll -d 1d20-2
    !roll a 1d20+4, 4d6, -d 1d20+3
```"""

    def run(self):
        bot = SlackHandler()

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

        def roll_die(number, sides):
            result = 0
            for x in range(0, number):
                result += random.randint(1, sides)
            return (result, "message")

        def advantage(number, sides):
            die_roll = max(roll_die(number, sides), roll_die(number, sides))
            message = "with advantage"
            return (die_roll, message)

        def disadvantage(number, sides):
            die_roll = min(roll_die(number, sides), roll_die(number, sides))
            message = "with disadvantage"
            return (die_roll, message)

        def build_final_result(roll_result, operator, modifier, roll_str, min_roll, max_roll):
            roll_plus_mods = "{} {} {}".format(
                    str(roll_result),
                    operator,
                    str(modifier)
            )
            mod_result = modifier if operator == "+" else modifier * -1
            result = int(roll_result[0]) + mod_result


            final_result = "*[ {} ]* _({} = {}) (min {}, max {})_ {}".format(
                    result,
                    roll_str,
                    roll_plus_mods,
                    min_roll + mod_result,
                    max_roll + mod_result,
                    message
                )

            return final_result


        def save_roll():
            pass

        valid_flags = {
            "a": advantage,
            "d": disadvantage,
            "save": save_roll
        }

        valid_operators = ["+", "-"]

        flag = None
        roll = roll_str.lstrip("-")
        operator = "+"
        modifier = 0

        for f in valid_flags:
            if roll_str.startswith(f):
                flag = f
                roll = roll[len(flag):]

        for o in valid_operators:
            if o in roll:
                operator = o
                roll, modifier = roll.split(o)

        modifier = int(modifier)
        number, sides = map(int, roll.split("d"))
        min_roll = number
        max_roll = sides * number

        roll_result, message = valid_flags[flag](number, sides) if flag else roll_die(number, sides)
        return build_final_result(roll_result, operator, modifier, roll_str, min_roll, max_roll)

    
    # def process_roll(self, roll_str):
    #     # import random

    #     def roll_die(number, sides):
    #         result = 0
    #         for x in range(0, number):
    #             result += random.randint(1, sides)
    #         return result

    #     def advantage(number, sides):
    #         die_roll = max(roll_die(number, sides), roll_die(number, sides))
    #         message = "with advantage"
    #         return (die_roll, message)

    #     def disadvantage(number, sides):
    #         die_roll = min(roll_die(number, sides), roll_die(number, sides))
    #         message = "with disadvantage"
    #         return (die_roll, message)

    #     valid_flags = {"a": advantage, "d": disadvantage}
    #     roll = ""
    #     operator = "+"
    #     modifier = 0
    #     flag = None
    #     message = ""

    #     if roll_str[0] == "-":
    #         roll_str = roll_str[1:]

    #     if roll_str[0] in valid_flags:
    #         flag = roll_str[0]
    #         roll_str = roll_str[1:]

    #     if "+" in roll_str:
    #         roll, modifier = roll_str.split("+")
    #     elif "-" in roll_str:
    #         operator = "-"
    #         roll, modifier = roll_str.split("-")
    #     else:
    #         roll = roll_str

    #     number, sides = roll.split("d")
    #     modifier = int(modifier)
    #     number = int(number)
    #     sides = int(sides)
    #     min_roll = number
    #     max_roll = sides * number

    #     if flag:
    #         roll_result, message = valid_flags[flag](number, sides)
    #     else:
    #         roll_result = roll_die(number, sides)

    #     roll_plus_mods = "{} {} {}".format(
    #             str(roll_result),
    #             operator,
    #             str(modifier)
    #     )

    #     mod_result = modifier if operator == "+" else modifier * -1
    #     result = roll_result + mod_result

    #     final_result = "*[ {} ]* _({} = {}) (min {}, max {})_ {}".format(
    #             result,
    #             roll_str,
    #             roll_plus_mods,
    #             min_roll + mod_result,
    #             max_roll + mod_result,
    #             message
    #         )

    #     return final_result

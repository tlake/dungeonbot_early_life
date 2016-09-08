from dungeonbot.plugins.primordials import BangCommandPlugin
from dungeonbot.handlers.slack import SlackHandler

from dungeonbot.plugins.die_roll import DieRoll


class RollPlugin(BangCommandPlugin):
    """Plugin for roll."""

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
        """Run roll plugin."""
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
        """Process Roll string."""
        r = DieRoll(roll_str)
        result = r.action()
        return r.print_results(result)

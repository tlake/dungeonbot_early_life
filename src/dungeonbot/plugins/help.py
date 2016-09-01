from dungeonbot.plugins.primordials import BangCommandPlugin
from dungeonbot.plugins import (
    karma,
    roll,
)


class HelpPlugin(BangCommandPlugin):
    help_topics = {
        'karma': karma.KarmaPlugin,
        'karma_newest': karma.KarmaNewestPlugin,
        'karma_top': karma.KarmaTopPlugin,
        'karma_bottom': karma.KarmaBottomPlugin,
        'roll': roll.RollPlugin,
    }

    help_text = """```
available help topics:
    help
    karma
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

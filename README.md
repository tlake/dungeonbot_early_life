# dungeonbot

A small Slack bot API written in Python for the _Import Campaign_ D&D campaign.


## About

DungeonBot uses Slack's [Events API](https://api.slack.com/events) to listen
for posts in channels and then acts upon them if appropriate using the
[slacker](https://github.com/os/slacker) Python library. Interaction is
primarily done through `!` commands, although there are (plans for) exceptions.


### `!` Commands

!help
 - Displays the help text, or help on a specific command if one is supplied.

!roll
 - Rolls dice.


### Future Plans & Features

Karma
 - `STRING++` or `STRING--` adds one positive or negative karma to STRING
 - `!karma STRING` prints total/positive/negative karma for STRING

More Robust `!roll`
 - `!roll save KEY VALUE`
 - `!roll KEY`
 - `!roll delete KEY`

Campaign Highlights
 - `!log add STRING` saves a timestamped STRING
 - `!log list [INT]` prints out the most recent (or INT most recent) highlight(s)

Miscellaneous Player K/V Storage
 - `!attr set KEY VALUE` creates/updates KEY with VALUE
 - `!attr get KEY`
 - `!attr list`
 - `!attr delete KEY`

## Contributing

If you've got an idea for a plugin, feel free to fork and submit a merge
request.

### _Quickstart Tips:_

Plugin logic lives inside classes defined in `plugins.py`; these classes
inherit from the `Plugin()` parent class, which gives them access to 
the `event` dict and `arg_string`. Make sure to define a `help()` method
to display help text and a `run()` method that contains your plugin logic:

```
class YourNewPlugin(Plugin):
    def help(self):
        bot = handlers.SlackHandler()
        help_text = "DEFINE HELP TEXT HERE"
        bot.make_post(self.event, help_text)

    def run(self):
        # PLUGIN LOGIC GOES HERE
```

_The method for posting to Slack can be seen above in the `help()` function:
just `import handlers`, instantiate the `SlackHandler()`, and call that
handler's `make_post()` method with the `event` dict and the message to be
posted._

Make sure that `HelpPlugin()` is the last class in the file.

You must also update the `EventHandler()` class's `valid_commands` in
`handlers.py` in order for your new plugin to work:

```
valid_commands = {
    # . . .
    'name_of_command': plugins.YourNewPlugin,
    }
```

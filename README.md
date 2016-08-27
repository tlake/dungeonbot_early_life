# dungeonbot

A small Slack bot API written in Python for the _Import Campaign_ D&D campaign.


## About

DungeonBot uses Slack's [Events API](https://api.slack.com/events) to listen
for posts in channels and then acts upon them if appropriate using the
[slacker](https://github.com/os/slacker) Python library. Interaction is
primarily done through `!` commands, although there are (plans for) exceptions.


## Contributing

Want to help out? We track stuff that needs doing over in
[issues](https://github.com/tlake/dungeonbot/issues). Feel free to submit pull
requests to the `dev` branch, and be sure to reference the issue number that
you're working on.

Please be sure to update any relevant help text and resolve any potential merge
conflicts, and try to be PEP8 compliant.


#### Setup

It's Python3, so you'll wanting an appropriate virtual environment and to
`pip install -r pipreqs.txt`. You can stand up a local instance of the server
with `python main.py`.

_Note: Without `BOT_ACCESS_TOKEN` and `PERMISSION_TO_SPEAK` properly exported
as environment variables, the SlackHandler in handlers.py won't be able to
authenticate. That's why there are a couple of switches in SlackHandler that
provide alternatives if you haven't explicitly configured the server to
speak to Slack._

#### Sending Requests To A Local Server

`auxiliaries/send_dummy_event.sh` contains an example `curl` command that will
make a mock request. Use it as a template to make your own requests; the value
of `"text"` represents the contents of a message posted in Slack, so you'll
want to use that to test any new commands.

Personally, I find it easier to use Postman to make a POST request. The
`Content-type` header obviously goes in Postman's Headers, and the entire
JSON blob can be pasted into Postman's Body (select the *raw* radio button
and choose the JSON option form the dropdown) once you strip off the two
enclosing single quotes. Point Postman to `localhost:5006`.


#### Quickstart

Plugin logic lives inside classes defined in `plugins.py`; these classes
inherit from the `Plugin()` parent class, which gives them access to 
the `event` dict and `arg_string`, as well as a default 'help' response.
Make sure to define `help_text` at the top of the plugin and a `run()`
method that contains your plugin logic,

Need your plugin to post to Slack? Just `import handlers`, instantiate the
`SlackHandler()`, and call that handler's `make_post()` method with the
`event` dict and the message to be posted.

```
class YourNewPlugin(Plugin):
    help_text = "DEFINE HELP TEXT HERE"

    def run(self):
        # PLUGIN LOGIC GOES HERE
        
        message = "I need this to go to Slack."
        import handlers
        bot = SlackHandler()
        bot.make_post(event, message)
```

Make sure that `HelpPlugin()` is the last class in the file.

You must also update the `EventHandler()` class's `valid_commands` in
`handlers.py` in order for your new plugin to work:

```
valid_commands = {
    # . . .
    'name_of_command': plugins.YourNewPlugin,
    }
```

It would also be helpful to add an entry to `HelpPlugin()`'s `help_text` so
that people will know that your plugin exists when they run `!help`.

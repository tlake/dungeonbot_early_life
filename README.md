# dungeonbot

A small Slack bot API written in Python for the _Import Campaign_ D&D campaign.


## About

DungeonBot uses Slack's [Events API](https://api.slack.com/events) to listen
for posts in channels and then acts upon them if appropriate using the
[slacker](https://github.com/os/slacker) Python library. Interaction is
primarily done through `!` commands, although there are (plans for) exceptions.


## Contributing

We track stuff that needs doing over in
[issues](https://github.com/tlake/dungeonbot/issues).

Want to help out? Great! Here's how:

- Check out a new branch for your work from `dev` branch.
- Do your thing.
- When your changes are ready to be merged back into `dev` branch, do a
  `git pull --rebase` from `dev` to make sure your branch is up to date with
  the most recent `dev` and to replay your changes over the updated `dev` work.
- Resolve any merge conflicts, of course, and push your updated branch.
- Use `git rebase -i HEAD~x` (where `x` is the number of recent commits you
  would like to see) to clean up your commit history; the goal is to squish
  your work into a clean and sensible flow, and to weed out things like five
  consecutive "typo fix" commits.
- Force-push your cleaned-up personal branch (I don't care about rewriting
  history in these small auxiliary branches - I'd rather have a cleaner,
  easier-to-follow history in `master`).
- Make a pull request from your new branch back into `dev`.
     - If your work addresses an issue, please reference it in the body of
       the MR.
     - If your work resolves an issue, please use Git's issue-resolution
       keywords in the body of the MR (examples: `closes #1`, `fixes #1`, etc.)

Please be sure to update any relevant help text, and try to be PEP8 compliant.


### Developer Project Overview

The innermost `dungeonbot/` directory is the robot proper; it contains all of
DungeonBot's brains and guts. The app object itself is created in
`dungeonbot/app_config.py` and the API routes are defined within
`dungeonbot/routes.py`. `dungeonbot/` is configured to be a module, and so
the app config and the routing are both imported into `dungeonbot/__init__.py`.
From there, the logic chain proceeds through `dungeonbot/handlers/*.py`, which
parses the Slack input and spins up the appropriate plugin in
`dungeonbot/plugins/*.py`. Additionally, database models live in
`dungeonbot/models.py`, and `dungeonbot/oauth.py` exists to allow teams to
integrate DungeonBot.

Outside of the `dungeonbot` module, `manage.py` will likely be the primary
interface for interacting with the bot while developing, and `auxiliaries/`
contains a small suite of files that may be of use during development.

#### Setup

##### Environment

It's Python3, so you'll be wanting an appropriate virtual environment and to
`pip install -r pipreqs.txt`.

##### Database

DungeonBot uses a locally-served PostgreSQL database in production, and is
managed with the [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org)
extension.

You'll need to install PostgreSQL on your machine if you haven't already;
probably something like `apt-get install postgres` or `brew install postgres`.
Once the DB server is up and running locally, you'll want to make a new
database with `createdb dungeonbot_db`. From there, you'll be interacting with
`manage.py` (see [Flask-Script](https://flask-script.readthedocs.io/en/latest/)
for more information on how that file works).

**Note:** You'll need to configure the environment variables `DB_USER` and
`DB_PASS` to be the same credentials that you would use to access the
PostgreSQL database manually.

Run `python manage.py db init` to initialize the new database. 
 - `manage.py` is executable as well, so you can also just call it directly
   and omit the `python` part: `./manage.py db init`, for example, if you're
   in the same directory

[Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) is used to
manage migrations. Once changes have been made to any models, run
`manage.py db migrate` to create the migrations, and then
`manage.py db upgrade` to apply them.

Migrations are automatically stored in `migrations/`, and these files ought to
be committed to the repository in order to maintain the integrity of the
production database.

##### Running Locally

Once everything has been set up, you can run a local instance of the server
with `manage.py runserver`. You will then be able to successfully send POST
requests to the server at `localhost:5006`.

`auxiliaries/send_dummy_event.sh` contains an example `curl` command that will
make a mock request. You can use it as a template to make your own requests;
the value of `"text"` represents the contents of a message posted in Slack,
so you'll want to use that to test any new commands.

Personally, I find it easier to use Postman to make a POST request. The
`Content-type` header obviously goes in Postman's Headers, and the entire
JSON blob can be pasted into Postman's Body (select the *raw* radio button
and choose the JSON option form the dropdown) once you strip off the two
enclosing single quotes. Point Postman to `localhost:5006`.

Access to a Python interpreter with some already-provided imports can be
achieved with `manage.py shell`. See the contents of `manage.py` to get an
idea of what that environment looks like.


#### Plugin Quickstart

##### Make The Plugin Itself

Plugin logic lives inside classes defined in `plugins/*.py`; these classes
inherit from parent classes defined in `plugins/primordials.py`, which gives
them access to things like the `event` dict and `arg_string`, as well as a
default 'help' response. Make sure to define `help_text` at the top of the
plugin and a `run()` method that contains your plugin logic.

Need your plugin to post to Slack? Just use
`from dungeonbot.handlers.slack import SlackHandler`, instantiate the
`SlackHandler()`, and call that handler's `make_post()` method with the
`event` dict and the message to be posted.

```
from dungeonbot.handlers.slack import SlackHandler


class YourNewPlugin(Plugin):
    help_text = "DEFINE HELP TEXT HERE"

    def run(self):
        # PLUGIN LOGIC GOES HERE
        
        message = "I need this to go to Slack."
        bot = SlackHandler()
        bot.make_post(self.event, message)
```

##### Add Plugin To The Event Handler

Update the `EventHandler()` class's `valid_commands` (or `valid_suffixes`, if
you're making a suffix-command plugin) in `dungeonbot/handlers/event.py`:

```
from dungeonbot.plugins import (
    # . . .
    your_new_plugin_module
)

class EventHandler(object):
    # . . .
    def parse_bang_command(self):
        valid_commands = {
            # . . .
            'name_of_command': your_new_plugin_module.YourNewPlugin,
        }
    # . . .
```

##### Add Plugin To The Help Plugin

Update the `HelpPlugin()` found in `dungeonbot/plugins/help/` with information
about your plugin: both its commands, and its help text:

```
from dungeonbot.plugins.your_new_plugin_module import YourNewPlugin

class HelpPlugin(BangCommandPlugin):
    help_topics = {
        # . . .
        'your_plugin_command': YourNewPlugin,
    }

    help_text = """```
available help topics:
    # . . .
    your_plugin_command
```

#### Model Quickstart

```
class ExampleModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(128))

    @classmethod
    def new(cls, text=None, session=None):
        if session is None:
            session = db.session
        instance = cls(text=text)
        session.add(instance)
        session.commit()
        return instance
```

_Using class methods on a model (like `new()` above) allows for database
actions to be wrapped up and contained within the model itself in a very nice,
object-oriented manner._

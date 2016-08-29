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
- Resolve any merge conflicts, of course.
- Squash your commits into a single commit (I find `git rebase -i HEAD~x` to be
  particularly helpful, where `x` is something close to the number of commits
  that you've made).
- Give your new single commit a good descriptive title, and write more stuff
  in the body if you'd like.
- Force-push that new squashed commit to your personal branch (I don't care
  about rewriting history in these small auxiliary branches - I'd rather have
  a cleaner, easier-to-follow history in `master`).
- Make a merge request from your new branch back into `dev`.
     - If your work addresses an issue, please reference it in the body of
       the MR.
     - If your work resolves an issue, please use Git's issue-resolution
       keywords in the body of the MR (examples: `closes #1`, `fixes #1`, etc.)

Please be sure to update any relevant help text, and try to be PEP8 compliant.


### Developer Project Overview

The innermost `dungeonbot/` directory is the robot proper; it contains all of
DungeonBot's brains and guts. `dungeonbot/` is configured to be a module, and
as such, the configuration and routing of the Flask app is contained within
`dungeonbot/__init__.py`. From there, the logic chain proceeds through
`dungeonbot/handlers.py`, which parses the Slack input and spins up the
appropriate plugin in `dungeonbot/plugins.py`. Additionally, database models
live in `dungeonbot/models.py`, and `dungeonbot/oauth.py` exists to allow
teams to integrate DungeonBot.

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


#### Plugin Quickstart

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


#### Model Quickstart

```
class ExampleModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(128))

    def __init__(self, text):
        self.text = text

    @classmethod
    def write(cls, text=None):
        instance = cls(text=text)
        db.session.add(instance)
        db.session.commit()
        return instance
```

_Using class methods on a model (like `write()` above) allows for database
actions to be wrapped up and contained within the model itself in a very nice,
object-oriented manner._

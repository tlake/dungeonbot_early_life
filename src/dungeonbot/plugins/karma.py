from dungeonbot.plugins.primordials import (
    BangCommandPlugin,
    SuffixCommandPlugin,
)
# from dungeonbot.handlers import SlackHandler
from dungeonbot.models import KarmaModel


class KarmaAssistant(object):
    def check_if_correlates_to_userid(self, event, possible_username):
        """Returns a Slack user ID or None"""

        from dungeonbot.handlers import SlackHandler

        bot = SlackHandler()
        user_id = bot.get_userid_from_name(possible_username)

        # If we get an id back, let's make sure it's from the same team as
        # the team from which the event originated.
        if user_id:
            user_obj = bot.get_user_obj_from_id(user_id)
            user_team = user_obj['team_id']
            if user_team == event['team_id']:
                return user_id

    def check_if_correlates_to_username(self, event, possible_userid):
        """Returns a Slack username or None"""

        from dungeonbot.handlers import SlackHandler

        bot = SlackHandler()
        username = bot.get_user_from_id(possible_userid)

        # If we get a username back, let's make sure it's from the same team as
        # the team from which the event originated.
        if username:
            user_obj = bot.get_user_obj_from_id(possible_userid)
            user_team = user_obj['team_id']
            if user_team == event['team_id']:
                return username


class KarmaModifyPlugin(SuffixCommandPlugin):
    def run(self):
        """
        self.arg_string: just a string that's getting karma
        self.suffix: '++' or '--'

        Should check if the arg_string is a string that correlates to a userid.
        If so, attribute the karma to that userid. Otherwise, just use the
        string.
        """
        ka = KarmaAssistant()
        possible_userid = ka.check_if_correlates_to_userid(
            self.event,
            self.arg_string
        )

        karma_subject = possible_userid if possible_userid else self.arg_string

        upvotes = 1 if self.suffix == '++' else 0
        downvotes = 1 if self.suffix == '--' else 0

        KarmaModel.modify(
            string_id=karma_subject,
            upvotes=upvotes,
            downvotes=downvotes,
        )


class KarmaPlugin(BangCommandPlugin):
    help_text = '\n'.join([
        "```",
        "command:",
        "    !karma",
        "",
        "description:",
        "    A system for tracking imaginary internet points.",
        "",
        "    For any string (whitespace-inclusive), you can award positive or",
        "    negative karma by appending '++' or '--' to the end.",
        "",
        "    Calling the '!karma' command with a specific string as an",
        "    argument will display the karma for the string, if it exists.",
        "",
        "    The karma system also has the following additional features:",
        "",
        "    karma_newest",
        "    karma_top",
        "    karma_bottom",
        "",
        "    More information can be found with '!help <FEATURE>'.",
        "",
        "usage:",
        "    <STRING>++",
        "    <STRING>--",
        "    !karma <STRING>",
        "",
        "    (<PARAMS> are required; [PARAMS] are optional)",
        "",
        "examples:",
        "    dungeonbot++",
        "    slack teams without dungeonbot--",
        "    !karma dungeonbot",
        "    !karma slack teams without dungeonbot",
        "```",
    ])

    def run(self):
        """
        Before querying, should check if the target is a string that correlates
        to a userid. If so, query the database using that userid. Otherwise,
        just use the target string.

        In every possible case, for each result returned, should check if the
        record's string_id is actually a Slack userid that correlates to a
        username. If so, use the username in the message posted to Slack.
        Otherwise, use the record's string_id.
        """

        from dungeonbot.handlers import SlackHandler
        bot = SlackHandler()
        KA = KarmaAssistant()

        possible_userid = KA.check_if_correlates_to_userid(
            self.event,
            self.arg_string,
        )

        karma_subject = possible_userid if possible_userid else self.arg_string

        karma_entry = KarmaModel.get_by_name(karma_subject)
        entry_name = karma_entry['string_id']

        possible_username = KA.check_if_correlates_to_username(
            self.event,
            entry_name,
        )

        subject_name = possible_username if possible_username else entry_name

        message = "*{}* has *{}* karma _({} ++, {} --)_".format(
            subject_name,
            karma_entry.karma,
            karma_entry.upvotes,
            karma_entry.downvotes,
        )

        bot.make_post(self.event, message)


class KarmaNewestPlugin(BangCommandPlugin):
    help_text = """```
command:
    !karma_newest

description:
    Returns the n most recently-created karma subjects, where n=5 unless
    otherwise provided.

usage:
    !karma_newest [INT]

    (<PARAMS> are required; [PARAMS] are optional)

examples:
    !karma_newest
    !karma_newest 10
```"""


class KarmaTopPlugin(BangCommandPlugin):
    help_text = """```
command:
    !karma_top

description:
    Returns the n highest-rated karma subjects, where n=5 unless
    otherwise provided.

usage:
    !karma_top [INT]

    (<PARAMS> are required; [PARAMS] are optional)

examples:
    !karma_top
    !karma_top 10
```"""


class KarmaBottomPlugin(BangCommandPlugin):
    help_text = """```
command:
    !karma_bottom

description:
    Returns the n lowest-rated karma subjects, where n=5 unless
    otherwise provided.

usage:
    !karma_bottom [INT]

    (<PARAMS> are required; [PARAMS] are optional)

examples:
    !karma_bottom
    !karma_bottom 10
```"""

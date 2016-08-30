from dungeonbot.plugins.primordials import HybridCommandPlugin
from dungeonbot.handlers import SlackHandler


class KarmaPlugin(HybridCommandPlugin):
    def run(self):
        if self.suffix:
            self.update_karma()
        else:
            self.retrieve_karma()

    def update_karma(self):
        bot = SlackHandler()
        user_id = bot.get_userid_from_name(self.arg_string)

        if user_id:
            user_obj = bot.get_user_obj_from_id(user_id)
            if user_obj['team_id'] == self.event['team_id']:
                attr_string = user_id
        else:
            attr_string = self.arg_string

        

    def retrieve_karma(self):
        pass

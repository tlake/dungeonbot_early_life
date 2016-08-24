from slacker import Slacker
import os


def make_post(request):
    BOT = Slacker(os.getenv("BOT_ACCESS_TOKEN"))

    BOT.chat.post_message(
        request.json['event']['channel'],
        request.json['event']['text'],
        as_user=True,
    )

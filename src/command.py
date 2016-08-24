from common import make_post


VALID_COMMANDS = [
    "help",
]


def parse_command(event):
    command, args = event['text'].split(' ', 1)

    if command not in VALID_COMMANDS:
        make_post("Sorry, {} is not a valid command.".format(command))

    else:
        make_post("{} is totes a valid command!".format(command))

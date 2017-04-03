import os
from slacker import Slacker


SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
BOT_NAME = "dungeonbot"

s = Slacker(SLACK_BOT_TOKEN)


if __name__ == "__main__":
    print(s.users.get_user_id(BOT_NAME))

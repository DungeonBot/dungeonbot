"""Define the SlackHandler class."""

import os
from slacker import Slacker
from auxiliaries.helpers import eprint


class SlackHandler(object):
    """Handle interacting with Slack."""

    def __init__(self):
        """Initialize SlackHandler with a Slacker connection.

        `self.vocal` is set based upon the environment variable
        "PERMISSION_TO_SPEAK". If this is False, SlackHandler will
        print to stdout instead of posting directly to Slack.

        """
        self.slack = Slacker(os.environ.get("BOT_ACCESS_TOKEN"))
        self.vocal = os.getenv("PERMISSION_TO_SPEAK")

    def make_post(self, event, message):
        """Post a message to Slack."""
        if self.vocal:
            self.slack.chat.post_message(
                event['channel'],
                message,
                as_user=True,
            )

        else:
            message = '\n\n' + message + '\n'
            eprint("Message that would have been sent to Slack:", message)

    def get_userid_from_name(self, username):
        """Lookup Slack user ID given username."""
        if self.vocal:
            return self.slack.users.get_user_id(username)
        else:
            return "A_SLACK_USERID"

    def get_username_from_id(self, user_id):
        """Lookup Slack username given user ID."""
        if self.vocal:
            user_obj = self.get_user_obj_from_id(user_id)
            return user_obj['name'] if user_obj else None
        else:
            return "A_SLACK_USERNAME"

    def get_user_obj_from_id(self, user_id):
        """Fetch a user dict object from Slack."""
        members_dict = self._fetch_user_obj(user_id)
        for entry in members_dict:
            if user_id in entry['id']:
                return entry

    def _fetch_user_obj(self, user_id):
        if self.vocal:
            return self.slack.users.list().body['members']

        else:
            return {
                'color': '99a949',
                'deleted': False,
                'id': 'SLACK_USERID',
                'is_admin': False,
                'is_bot': True,
                'is_owner': False,
                'is_primary_owner': False,
                'is_restricted': False,
                'is_ultra_restricted': False,
                'name': 'example_dungeonbot',
                'profile': {
                    'api_app_id': '',
                    'avatar_hash': 'some_hash',
                    'bot_id': 'SLACK_BOT_ID',
                    'first_name': 'Dungeon',
                    'image_1024': 'https://img_url.png',
                    'image_192': 'https://img_url.png',
                    'image_24': 'https://img_url.png',
                    'image_32': 'https://img_url.png',
                    'image_48': 'https://img_url.png',
                    'image_512': 'https://img_url.png',
                    'image_72': 'https://img_url.png',
                    'image_original': 'https://img_url.png',
                    'last_name': 'Bot',
                    'real_name': 'Dungeon Bot',
                    'real_name_normalized': 'Dungeon Bot'
                },
                'real_name': 'Dungeon Bot',
                'status': None,
                'team_id': 'SLACK_TEAM_ID',
                'tz': None,
                'tz_label': 'Pacific Daylight Time',
                'tz_offset': -25200
            }

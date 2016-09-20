"""Tests for the Event Handler."""

from dungeonbot.conftest import BaseTest

from dungeonbot.handlers.event import EventHandler

from unittest import mock


# def mock_full_event():
#     """Create a full event as sent from Slack."""
#     return {
#         "event": {
#             "text": "!help",
#             "type": "message",
#             "user": "U1N796T52",
#             "ts": "1472164181.000061",
#             "channel": "C2377T63B",
#             "event_ts": "1472164181.000061",
#         },
#         "token": "y3vNnzVDQmsaU7123cifMrFj",
#         "team_id": "T1N7FEJHE",
#         "api_app_id": "A237E9UMB",
#         "type": "event_callback",
#         "authed_users": ["U248CQ9CP"],
#     }


class EventHandlerUnitTest(BaseTest):
    """Tests for the Event Handler."""

    def setUp(self):
        """Create an event as processed by the `/` route."""
        super().setUp()

        self.mock_event = {
            "text": "",
            "type": "message",
            "user": "U1N796T52",
            "ts": "1472164181.000061",
            "channel": "C2377T63B",
            "event_ts": "1472164181.000061",
            "team_id": "T1N7FEJHE",
        }

    def test_process_event_with_bang_command(self):
        """Assert parse_bang_command method is called."""
        mock_parser = mock.Mock(name="parse_bang_command")
        mock_parser.return_value = "Success"

        evt = self.mock_event
        evt["text"] = "!testing is great"

        with mock.patch.object(EventHandler,
                               'parse_bang_command',
                               mock_parser):
            handler = EventHandler(evt)
            handler.process_event()

            self.assertTrue(mock_parser.called)

    def test_process_event_with_suffix_command(self):
        """Assert parse_bang_command method is called."""
        mock_parser = mock.Mock(name="parse_suffix_command")
        mock_parser.return_value = "Success"

        evt = self.mock_event
        evt["text"] = "testing++"

        with mock.patch.object(
            EventHandler,
            'parse_suffix_command',
            mock_parser
        ):
            handler = EventHandler(evt)
            handler.process_event()

            self.assertTrue(mock_parser.called)

    def test_valid_parse_bang_command(self):
        """Test parse_bang_command method when valid."""
        evt = self.mock_event

        mock_commands = {
            'help': mock.Mock(name="MockHelpPlugin"),
            'karma': mock.Mock(name="MockKarmaPlugin"),
            'karma_newest': mock.Mock(name="MockKarmaNewestPlugin"),
            'karma_top': mock.Mock(name="MockKarmaTopPlugin"),
            'karma_bottom': mock.Mock(name="MockKarmaBottomPlugin"),
            'roll': mock.Mock(name="MockRollPlugin"),
            'quest': mock.Mock(name="MockQuestPlugin"),
        }

        for key in mock_commands.keys():
            evt['text'] = "!" + key
            handler = EventHandler(evt)

            with mock.patch.object(
                handler,
                "valid_commands",
                mock_commands,
            ):
                handler.parse_bang_command()
                self.assertTrue(mock_commands[key].called)

    def test_invalid_parse_bang_command(self):
        """Test parse_bang_command method when invalid."""
        evt = self.mock_event
        evt['text'] = "!INVALIDCOMMAND"
        handler = EventHandler(evt)

        mock_bot = mock.Mock(name="mock_bot")
        mock_commands = {
            'help': mock.Mock(name="MockHelpPlugin"),
            'karma': mock.Mock(name="MockKarmaPlugin"),
            'karma_newest': mock.Mock(name="MockKarmaNewestPlugin"),
            'karma_top': mock.Mock(name="MockKarmaTopPlugin"),
            'karma_bottom': mock.Mock(name="MockKarmaBottomPlugin"),
            'roll': mock.Mock(name="MockRollPlugin"),
            'quest': mock.Mock(name="MockQuestPlugin"),
        }

        with mock.patch.multiple(
            handler,
            bot=mock_bot,
            valid_commands=mock_commands,
        ):
            handler.parse_bang_command()
            self.assertTrue(mock_bot.make_post.called)

            for val in mock_commands.values():
                self.assertFalse(val.called)

    def test_valid_parse_suffix_command(self):
        """Test parse_suffix_command method when valid."""
        evt = self.mock_event

        mock_karma_modify_plugin = mock.Mock(name="MockKarmaModifyPlugin")

        mock_suffixes = {
            '++': mock_karma_modify_plugin,
            '--': mock_karma_modify_plugin,
        }

        for key in mock_suffixes.keys():
            evt['text'] = "a testing string" + key
            handler = EventHandler(evt)

            with mock.patch.object(
                handler,
                "valid_suffixes",
                mock_suffixes
            ):
                handler.parse_suffix_command()
                self.assertTrue(mock_suffixes[key].called)

    def test_invalid_parse_suffix_command(self):
        """Test parse_suffix_command method when invalid."""
        evt = self.mock_event
        evt['text'] = "a testing string"
        handler = EventHandler(evt)

        mock_karma_modify_plugin = mock.Mock(name="MockKarmaModifyPlugin")
        mock_suffixes = {
            '++': mock_karma_modify_plugin,
            '--': mock_karma_modify_plugin,
        }

        with mock.patch.object(
            handler,
            "valid_suffixes",
            mock_suffixes
        ):
            handler.parse_suffix_command()
            for val in mock_suffixes.values():
                self.assertFalse(val.called)

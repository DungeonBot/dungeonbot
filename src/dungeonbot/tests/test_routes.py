"""Tests for the routes module."""


from dungeonbot.conftest import BaseTest

from dungeonbot import routes

from unittest import mock

import json


class RoutesToolsUnitTests(BaseTest):
    """Tests for the utility functions in the routes module."""

    def test_event_is_important_bang_command(self):
        """event_is_important returns true for a bang command."""
        event = {"user": "not a bot", "text": "!bang command"}
        mock_getenv = mock.MagicMock()
        mock_getenv.return_value = "some bot id"

        with mock.patch.object(routes.os, "getenv", mock_getenv):
            self.assertTrue(routes.event_is_important(event))

    def test_event_is_important_suffix_command(self):
        """event_is_important returns true for suffix command."""
        event = {"user": "not a bot", "text": "suffix command++"}
        mock_getenv = mock.MagicMock()
        mock_getenv.return_value = "some bot id"

        with mock.patch.object(routes.os, "getenv", mock_getenv):
            self.assertTrue(routes.event_is_important(event))

    def test_event_is_not_important(self):
        """event_is_important returns false for not the above."""
        mock_getenv = mock.MagicMock()
        mock_getenv.return_value = "some bot id"

        with mock.patch.object(routes.os, "getenv", mock_getenv):
            event = {"user": "not a bot", "text": "not a thing"}
            self.assertFalse(routes.event_is_important(event))

            event = {"user": "not a bot", "text": "bad suffix +-"}
            self.assertFalse(routes.event_is_important(event))

    def test_process_event_with_important_event(self):
        """process_event should call the mock event handler."""
        event = {"user": "not a bot", "text": "suffix command++"}
        mock_eprint = mock.MagicMock()
        mock_event_handler = mock.MagicMock()

        with mock.patch.object(routes, "EventHandler", mock_event_handler):
            with mock.patch.object(routes, "eprint", mock_eprint):
                self.assertTrue(routes.event_is_important(event))

                routes.process_event(event)

                self.assertTrue(mock_event_handler.called)
                self.assertTrue(mock_event_handler(event).process_event.called)

    def test_process_event_with_unimportant_event(self):
        """process_event should call the mock event handler."""
        event = {"user": "not a bot", "text": "buttslol"}
        mock_eprint = mock.MagicMock()
        mock_event_handler = mock.MagicMock()

        with mock.patch.object(routes, "EventHandler", mock_event_handler):
            with mock.patch.object(routes, "eprint", mock_eprint):
                self.assertFalse(routes.event_is_important(event))

                routes.process_event(event)

                self.assertFalse(mock_event_handler.called)


class RoutesUnitTests(BaseTest):
    """Tests for the routing functions in the routes module."""

    def test_route_root_with_get(self):
        """Return a redirect when accessed via GET."""
        tc = self.app.test_client()
        self.assertEqual(302, tc.get('/').status_code)

    def test_route_root_with_post(self):
        """Return a 200 OK when accessed via POST."""
        tc = self.app.test_client()
        event = {"event": {"a thing": "something"}, "team_id": "some id"}
        mock_processor = mock.MagicMock()

        with mock.patch.object(routes, "process_event", mock_processor):
            # import ipdb; ipdb.set_trace()
            self.assertEqual(200, tc.post(
                '/',
                data=json.dumps(event),
                content_type="application/json",
            ).status_code)
            self.assertTrue(mock_processor.called)

    def test_route_oauth(self):
        """The OAuth route just returns 200 for now."""
        tc = self.app.test_client()
        self.assertEqual(200, tc.get('/oauth').status_code)

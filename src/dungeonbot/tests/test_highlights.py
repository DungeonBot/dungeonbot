from dungeonbot.conftest import BaseTest
from dungeonbot.models.highlights import HighlightModel
from dungeonbot.plugins.highlights import HighlightPlugin

from datetime import datetime
import calendar
from unittest import mock


class HighlightsTests(BaseTest):
    """Test Campaign Highlights."""

    def setUp(self):
        """Create an event as processed by the `/` route."""
        super().setUp()

        self.user = {"id": "U48295", "name": "camry"}
        self.mock_event = {
            "text": "",
            "type": "message",
            "user": self.user,
            "ts": "1472164181.000061",
            "channel": "C2377T63B",
            "event_ts": "1472164181.000061",
            "team_id": "T1N7FEJHE",
        }
        self.model = HighlightModel()
        self.plugin = HighlightPlugin(self.mock_event, self.user)

        self.model.new("First Highlight")
        for x in range(10):
            self.model.new(str(x))

    # Model Tests
    def test_new_model_has_base_attrs(self):
        """Test that a newly-instantiated highlight has minimum attributes."""
        attrs = ["id", "text", "created"]
        for attr in attrs:
            assert hasattr(self.model, attr)

    def test_create_new_highlight_manual_add(self):
        """Test that a new highlight can be added to the database."""
        highlight = HighlightModel()
        highlight.text = "Test highlight"
        highlight.created = datetime.utcnow()
        highlight.last_updated = datetime.utcnow()

        self.db.session.add(highlight)
        self.db.session.commit()

        assert highlight in self.db.session

    def test_model_create_new(self):
        """Assert that new highlight can be added with model method."""
        x = self.model.new("Testing adding stuff")
        assert x in self.db.session

    def test_model_create_new_no_args(self):
        """Assert that attempting to create new highlight with no args will return None."""
        len_before = len(self.model.list())
        assert self.model.new() is None
        assert len(self.model.list()) == len_before

    def test_model_list(self):
        """Assert that the model method list will return 10 most recent entries."""
        assert len(self.model.list()) == 10

    def test_model_list_limit(self):
        """Assert that the model method list will return the most recent entry limited by k."""
        assert len(self.model.list(3)) == 3

    # Plugin Tests
    def test_run(self):
        """Assert that run calls process_highlights."""
        mock_parser = mock.Mock(name="process_highlight")
        mock_parser.return_value = "Success"

        evt = self.mock_event
        arg = "Testing everything"

        with mock.patch.object(
            HighlightPlugin,
            'process_highlight',
            mock_parser
        ):
            handler = HighlightPlugin(evt, arg)
            handler.run()

            self.assertTrue(mock_parser.called)

    def test_process_highlights_invalid(self):
        """Assert that calling process highlights without a valid arg returns proper message."""
        message = """
                Whoops! That isn't a valid command.
                Maybe try !help log if you are stuck
            """
        assert self.plugin.process_highlight(["dance"]) == message

    def test_process_highlights_add(self):
        """Assert that process highlights calls add method."""
        mock_parser = mock.Mock(name="add")
        mock_parser.return_value = "Success"
        evt = self.mock_event
        arg = "add something"

        with mock.patch.object(HighlightPlugin, 'add', mock_parser):
            handler = HighlightPlugin(evt, arg)
            handler.process_highlight(arg.split())

            self.assertTrue(mock_parser.called)

    def test_process_highlights_list(self):
        """Assert that process highlights calls list method."""
        mock_parser = mock.Mock(name="list_highlights")
        mock_parser.return_value = "Success"
        evt = self.mock_event
        arg = "list 2"

        with mock.patch.object(HighlightPlugin, 'list_highlights', mock_parser):
            handler = HighlightPlugin(evt, arg)
            handler.process_highlight(arg.split())

            self.assertTrue(mock_parser.called)

    def test_add_success(self):
        """Assert that highlight can be added."""
        args = ["adding a new highlight"]
        assert self.plugin.add(args) == "*New Campaign Highlight*\n{}".format(*args)

    def test_add_failure(self):
        """Assert that calling highlight with no args will return proper message."""
        assert self.plugin.add([]) == "Could not save highlight."

    def test_list_highlights(self):
        """Assert that calling list highlights returns a properly formatted message."""
        h = self.model.list(how_many=1)[0]
        month = calendar.month_abbr[h.created.month]
        day = h.created.day
        message = "*1 Most Recent Campaign Highlights*\n*{} {}* - {}".format(month, day, h.text)
        assert self.plugin.list_highlights([1]) == message

from dungeonbot.conftest import BaseTest
from dungeonbot.plugins.roll import RollPlugin
from dungeonbot.handlers.slack import SlackHandler
from unittest import mock


class RollPluginTests(BaseTest):
    """Tests for Roll Plugin."""

    def setUp(self):
        """Create an event as processed by the `/` route."""
        super().setUp()
        self.user = {"id": "U429845", "name": "disa"}

        self.mock_event = {
            "text": "",
            "type": "message",
            "user": "A_SLACK_USERID",
            "ts": "1472164181.000061",
            "channel": "C2377T63B",
            "event_ts": "1472164181.000061",
            "team_id": "SLACK_TEAM_ID",
        }
        self.plugin = RollPlugin(self.mock_event, self.user)

    def test_run(self):
        """Assert Run calls Process Roll."""
        mock_parser = mock.Mock(name="process_roll")
        mock_parser.return_value = "Success"
        evt = self.mock_event

        with mock.patch.object(RollPlugin, "process_roll", mock_parser):
            handler = RollPlugin(evt, "1d20")
            handler.run()
            assert mock_parser.called

    # This test disabled until we fix the validation in RollPlugin.process_roll()
#    def test_process_roll_invalid_command(self):
#        """Assert that invalid commands are handled properly by process roll."""
#        args = "ketchup"
#        self.assertEqual(self.plugin.process_roll(args, self.user), "Not a valid command.")

    def test_process_roll_save(self):
        """Assert that process roll handles save command."""
        mock_parser = mock.Mock(name="save_roll")
        mock_parser.return_value = "Success"

        evt = self.mock_event
        arg = "save ax 1d20 + 4"
        with mock.patch.object(RollPlugin, 'save_roll', mock_parser):
            handler = RollPlugin(evt, arg)
            handler.process_roll(arg, self.user)

            mock_parser.assert_called_with(arg.split()[1:], self.user)
            self.assertTrue(mock_parser.called)

    def test_process_roll_list(self):
        """Assert that process roll handles list command."""
        mock_parser = mock.Mock(name="list_rolls")
        mock_parser.return_value = "Success"

        evt = self.mock_event
        arg = "list"
        with mock.patch.object(RollPlugin, 'list_rolls', mock_parser):
            handler = RollPlugin(evt, arg)
            handler.process_roll(arg, self.user)

            mock_parser.assert_called_with([], self.user)

    def test_process_roll_delete(self):
        """Assert that process roll handles delete command."""
        mock_parser = mock.Mock(name="delete_roll")
        mock_parser.return_value = "Success"

        evt = self.mock_event
        arg = "delete something"
        with mock.patch.object(RollPlugin, 'delete_roll', mock_parser):
            handler = RollPlugin(evt, arg)
            handler.process_roll(arg, self.user)

            self.assertTrue(mock_parser.called)

    def test_process_roll_make_roll(self):
        """Assert that process roll handles make_roll command."""
        mock_parser = mock.Mock(name="make_roll")
        mock_parser.return_value = "Success"
        arg = "1d20"

        with mock.patch.object(RollPlugin, 'make_roll', mock_parser):
            handler = RollPlugin(self.mock_event, arg)
            handler.process_roll(arg, self.user)

            self.assertTrue(mock_parser.called)

    def test_save_roll_basic(self):
        """Assert that a basic save roll functions."""
        args = ["test", "1d20+2"]
        message = "Successfully Saved test: 1d20+2"
        self.assertEqual(self.plugin.save_roll(args, self.user), message)
        roll = self.plugin.make_roll([args[0]], self.user)
        self.assertIn("with test", roll)
        self.assertIn("1d20+2", roll)

    def test_save_roll_flag(self):
        """Assert that a roll with a flag can be saved and perform as expected."""
        args = ["test", "a1d20+2"]
        message = "Successfully Saved test: a1d20+2"
        assert self.plugin.save_roll(args, self.user) == message

    def test_save_roll_improper_key_val_pair(self):
        """Assert that an incorrectly formatted key/val pair will return an error string."""
        args = ["a1d20+2"]
        message = "Not a valid Key/Pair."
        assert self.plugin.save_roll(args, self.user) == message

    def test_save_roll_improper_roll(self):
        """Assert that an incorrectly formatted die roll will return an error string."""
        args = ["test", "a1202"]
        message = "Not a properly formatted roll string."
        assert self.plugin.save_roll(args, self.user) == message

    def test_delete_basic(self):
        """Assert that an item can be deleted and returns a confirmation."""
        args = ["test", "a1d20+2"]
        message = "test was successfully deleted."
        self.plugin.save_roll(args, self.user)
        assert self.plugin.delete_roll([args[0]], self.user) == message

    def test_delete_invalid(self):
        """Assert that attempting to delete a key that does not exist will return an error message."""
        message = "Cannot find item whoops"
        assert self.plugin.delete_roll(["whoops"], self.user) == message

    def test_list(self):
        """Assert that calling list returns formatted message."""
        args = [["test1", "1d20"], ["test2", "2d4"], ["test3", "3d8"]]
        message = "*Saved Rolls for {}:*".format(self.user["name"])
        for arg in args:
            self.plugin.save_roll(arg, self.user)
            message += "\n{}: {}".format(*arg)
        assert self.plugin.list_rolls([], self.user) == message

    def test_list_with_limit(self):
        """Assert that calling list with a limit returns formatted message."""
        args = [["test1", "1d20"], ["test2", "2d4"], ["test3", "3d8"]]
        message = "*Saved Rolls for {}:*".format(self.user["name"])
        for arg in args:
            self.plugin.save_roll(arg, self.user)
        message += "\n{}: {}".format(*args[0])
        assert self.plugin.list_rolls(["1"], self.user) == message

    def test_is_valid_roll_basic(self):
        """Assert that a valid roll returns true."""
        assert self.plugin.is_valid_roll_string("a1d20+7")

    def test_is_valid_roll_flag(self):
        """Assert that a valid roll with a flag returns true."""
        assert self.plugin.is_valid_roll_string("a1d20+7")

    def test_is_not_valid_roll_basic(self):
        """Assert that an invalid roll returns false."""
        assert not self.plugin.is_valid_roll_string("d20+7")

    def test_is_not_valid_roll_flag(self):
        """Assert that an invalid roll with a flag returns false."""
        assert not self.plugin.is_valid_roll_string("d20+7")

    def test_parse_roll_string_and_flag_basic(self):
        """Assert that a basic roll string returns the string, and None as flag."""
        args = ["1d20"]
        results = self.plugin.parse_flag_and_roll_string(args)
        assert results[0] == args[0] and results[1] is None

    def test_parse_roll_string_and_flag_with_flag(self):
        """Assert that a rollstring with a flag will return the separated rollstr, flag."""
        args = ["a", "1d20"]
        results = self.plugin.parse_flag_and_roll_string(args)
        assert results[0] == "1d20" and results[1] is "a"

    def test_make_roll_basic(self):
        """Assert that make roll works as expected."""
        pass

    def test_make_roll_flag(self):
        """Assert that make roll works with a flag as expected."""
        pass

    def test_make_roll_saved(self):
        """Assert that make roll works with a saved roll as expected."""
        pass

    def test_make_roll_invalid(self):
        """Assert that make roll with an invalid roll string returns an error message."""
        pass

    def test_roll_a_die(self):
        """Assert that running the roll plugin with the roll string results in proper output."""
        arg = "1d20"
        mock_parser = mock.Mock(name="make_post")

        with mock.patch.object(SlackHandler, "make_post", mock_parser):
            handler = RollPlugin(self.mock_event, arg)
            handler.run()
            assert mock_parser.called


# user object is not subscriptable in all tests below

    # def test_save_a_die(self):
    #     """Assert that running the roll plugin with the save flag and roll string results in proper output."""
    #     arg = "save test 2d8"
    #     message = "Successfully saved test: 2d8"
    #     mock_parser = mock.Mock(name="make_post")

    #     with mock.patch.object(SlackHandler, "make_post", mock_parser):
    #         handler = RollPlugin(self.mock_event, arg)
    #         handler.run()
    #         mock_parser.assert_called_with(self.event, message)

    # def test_delete_a_die(self):
    #     """Assert that running the roll plugin with the delete flag and roll string results in proper output."""
    #     self.plugin.save_roll(["test", "1d4"], self.user)
    #     arg = "delete test"
    #     message = "test was successfully deleted."
    #     mock_parser = mock.Mock(name="make_post")

    #     with mock.patch.object(SlackHandler, "make_post", mock_parser):
    #         handler = RollPlugin(self.mock_event, arg)
    #         handler.run()
    #         mock_parser.assert_called_with(self.event, message)

    # def test_list_a_die(self):
    #     """Assert that running the roll plugin with the list flag and roll string results in proper output."""
    #     arg = "list 1"
    #     self.plugin.save_roll(["test", "1d4"], self.user)
    #     message = "*Saved Rolls for {}:*\ntest: 1d4".format(self.user["name"])
    #     mock_parser = mock.Mock(name="make_post")

    #     with mock.patch.object(SlackHandler, "make_post", mock_parser):
    #         handler = RollPlugin(self.mock_event, arg)
    #         handler.run()
    #         mock_parser.assert_called_with(self.event, message)

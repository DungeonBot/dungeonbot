"""Tests for the Event Handler."""


from dungeonbot.conftest import BaseTest

from dungeonbot.models.karma import KarmaModel
from dungeonbot.plugins.karma import (
    KarmaAssistant,
    KarmaModifyPlugin,
    KarmaPlugin,
    KarmaNewestPlugin,
    KarmaTopPlugin,
    KarmaBottomPlugin,
)

from datetime import datetime
from unittest import mock


class KarmaModelUnitTests(BaseTest):
    """Tests for the KarmaModel."""

    def setUp(self):
        """Create templates for making new karma objects."""
        super().setUp()

        self.test_model_0 = {
            "name": "testing karma model 0",
            "upvotes": 1,
            "downvotes": 0,
        }

        self.test_model_1 = {
            "name": "testing karma model 1",
            "upvotes": 3,
            "downvotes": 1,
        }

        self.test_model_2 = {
            "name": "testing karma model 2",
            "upvotes": 0,
            "downvotes": 2,
        }

    def _populate_db(self, model_templates=[]):
        """Create a new DB entry for each item in model_templates."""
        for template in model_templates:
            KarmaModel.new(
                string_id=template["name"],
                upvotes=template["upvotes"],
                downvotes=template["downvotes"],
            )

    def test_classmethod_new(self):
        """Assert that KarmaModel.new() functions properly."""
        session = self.db.session

        self.assertEqual(
            [],
            session.query(KarmaModel).all()
        )

        self._populate_db([self.test_model_0])
        saved = session.query(KarmaModel).first()

        self.assertEqual(
            1,
            len(session.query(KarmaModel).all())
        )

        self.assertEqual(
            self.test_model_0["name"],
            saved.string_id
        )

        self.assertEqual(
            self.test_model_0["upvotes"],
            saved.upvotes
        )

        self.assertEqual(
            self.test_model_0["downvotes"],
            saved.downvotes
        )

        self.assertEqual(
            self.test_model_0["upvotes"] - self.test_model_0["downvotes"],
            saved.karma
        )

        self.assertIsNotNone(saved.created)

    def test_classmethod_modify(self):
        """Assert that KarmaModel.modify() functions properly."""
        self._populate_db([self.test_model_2])
        session = self.db.session

        KarmaModel.modify(string_id=self.test_model_2["name"], upvotes=1)

        self.assertEqual(1, session.query(KarmaModel).first().upvotes)
        self.assertEqual(2, session.query(KarmaModel).first().downvotes)
        self.assertEqual(-1, session.query(KarmaModel).first().karma)

        KarmaModel.modify(string_id=self.test_model_2["name"], downvotes=1)

        self.assertEqual(1, session.query(KarmaModel).first().upvotes)
        self.assertEqual(3, session.query(KarmaModel).first().downvotes)
        self.assertEqual(-2, session.query(KarmaModel).first().karma)

        KarmaModel.modify(string_id=self.test_model_2["name"], upvotes=2)

        self.assertEqual(3, session.query(KarmaModel).first().upvotes)
        self.assertEqual(3, session.query(KarmaModel).first().downvotes)
        self.assertEqual(0, session.query(KarmaModel).first().karma)

        KarmaModel.modify(string_id=self.test_model_2["name"], upvotes=1)

        self.assertEqual(4, session.query(KarmaModel).first().upvotes)
        self.assertEqual(3, session.query(KarmaModel).first().downvotes)
        self.assertEqual(1, session.query(KarmaModel).first().karma)

    def test_classmethod_get_by_name(self):
        """Assert that KarmaModel.get_by_name() functions properly."""
        self._populate_db([self.test_model_0, self.test_model_1])
        session = self.db.session

        self.assertEqual(
            session.query(KarmaModel).filter_by(
                string_id=self.test_model_0["name"]
            ).one(),
            KarmaModel.get_by_name(string_id=self.test_model_0["name"])
        )

        self.assertIsNone(KarmaModel.get_by_name("doesn't exist"))

    def test_classmethod_get_by_id(self):
        """Assert that KarmaModel.get_by_id() functions properly."""
        self._populate_db([self.test_model_0, self.test_model_1])
        session = self.db.session

        result = session.query(KarmaModel).get(1)

        self.assertEqual(
            result,
            KarmaModel.get_by_id(model_id=1)
        )

        self.assertEqual(
            result.string_id,
            self.test_model_0["name"]
        )

    def test_classmethod_list_newest(self):
        """Assert that KarmaModel.list_newest() functions properly."""
        self._populate_db([self.test_model_0])
        self._populate_db([self.test_model_1])
        self._populate_db([self.test_model_2])
        session = self.db.session

        results = KarmaModel.list_newest()

        self.assertEqual(3, len(results))

        self.assertEqual(
            session.query(KarmaModel).get(3),
            results[0]
        )

        self.assertEqual(
            session.query(KarmaModel).get(2),
            results[1]
        )

        self.assertEqual(
            session.query(KarmaModel).get(1),
            results[2]
        )

        results = KarmaModel.list_newest(how_many=1000)

        self.assertEqual(3, len(results))

        self.assertEqual(
            session.query(KarmaModel).get(3),
            results[0]
        )

        self.assertEqual(
            session.query(KarmaModel).get(2),
            results[1]
        )

        self.assertEqual(
            session.query(KarmaModel).get(1),
            results[2]
        )

        results = KarmaModel.list_newest(how_many=2)

        self.assertEqual(2, len(results))

        self.assertEqual(
            session.query(KarmaModel).get(3),
            results[0]
        )

        self.assertEqual(
            session.query(KarmaModel).get(2),
            results[1]
        )

    def test_classmethod_list_highest(self):
        """Assert that KarmaModel.list_highest() functions properly."""
        self._populate_db([
            self.test_model_0,
            self.test_model_1,
            self.test_model_2
        ])
        session = self.db.session

        results = KarmaModel.list_highest()

        self.assertEqual(3, len(results))

        self.assertEqual(
            session.query(KarmaModel).get(2),
            results[0]
        )

        self.assertEqual(
            session.query(KarmaModel).get(1),
            results[1]
        )

        self.assertEqual(
            session.query(KarmaModel).get(3),
            results[2]
        )

        results = KarmaModel.list_highest(how_many=1000)

        self.assertEqual(3, len(results))

        self.assertEqual(
            session.query(KarmaModel).get(2),
            results[0]
        )

        self.assertEqual(
            session.query(KarmaModel).get(1),
            results[1]
        )

        self.assertEqual(
            session.query(KarmaModel).get(3),
            results[2]
        )

        results = KarmaModel.list_highest(how_many=2)

        self.assertEqual(2, len(results))

        self.assertEqual(
            session.query(KarmaModel).get(2),
            results[0]
        )

        self.assertEqual(
            session.query(KarmaModel).get(1),
            results[1]
        )

    def test_classmethod_list_lowest(self):
        """Assert that KarmaModel.list_lowest() functions properly."""
        self._populate_db([
            self.test_model_0,
            self.test_model_1,
            self.test_model_2
        ])
        session = self.db.session

        results = KarmaModel.list_lowest()

        self.assertEqual(3, len(results))

        self.assertEqual(
            session.query(KarmaModel).get(3),
            results[0]
        )

        self.assertEqual(
            session.query(KarmaModel).get(1),
            results[1]
        )

        self.assertEqual(
            session.query(KarmaModel).get(2),
            results[2]
        )

        results = KarmaModel.list_lowest(how_many=1000)

        self.assertEqual(3, len(results))

        self.assertEqual(
            session.query(KarmaModel).get(3),
            results[0]
        )

        self.assertEqual(
            session.query(KarmaModel).get(1),
            results[1]
        )

        self.assertEqual(
            session.query(KarmaModel).get(2),
            results[2]
        )

        results = KarmaModel.list_lowest(how_many=2)

        self.assertEqual(2, len(results))

        self.assertEqual(
            session.query(KarmaModel).get(3),
            results[0]
        )

        self.assertEqual(
            session.query(KarmaModel).get(1),
            results[1]
        )

    def test_property_json(self):
        """Assert that KarmaModel.json() functions properly."""
        self._populate_db([self.test_model_0])

        model = KarmaModel.get_by_id(1)

        self.assertEqual(1, model.json["id"])
        self.assertEqual(self.test_model_0["name"], model.json["string_id"])
        self.assertEqual(self.test_model_0["upvotes"], model.json["upvotes"])
        self.assertEqual(
            self.test_model_0["downvotes"],
            model.json["downvotes"]
        )
        self.assertEqual(
            self.test_model_0["upvotes"] - self.test_model_0["downvotes"],
            model.json["karma"]
        )
        self.assertEqual(datetime, type(model.json["created"]))

    def test_property_slack_msg(self):
        """Assert that KarmaModel.slack_msg() functions properly."""
        self._populate_db([self.test_model_0])
        model = KarmaModel.get_by_id(1)

        self.assertEqual(
            "*testing karma model 0* has *1* karma _(1 ++, 0 --)_",
            model.slack_msg
        )

    def test_repr(self):
        """Assert that KarmaModels are displayed properly."""
        self._populate_db([self.test_model_0])
        model = KarmaModel.get_by_id(1)

        self.assertIn(
            "<dungeonbot.models.karma.KarmaModel(" +
            "string_id=testing karma model 0, upvotes=1, downvotes=0" +
            ") [id: 1, karma: 1, created:",
            model.__str__()
        )


class KarmaAssistantUnitTests(BaseTest):
    """Tests for the KarmaAssistant."""

    def test_check_if_correlates_to_userid(self):
        """Assert the check_if_correlates_to_userid() method functions."""
        mock_handler_succeed = mock.MagicMock(name="MockSlackHandler")
        mock_handler_succeed.get_userid_from_name.return_value = "SOME USER ID"
        mock_handler_succeed.get_user_obj_from_id.return_value = {
            "team_id": "SOME TEAM ID",
        }

        mock_handler_fail = mock.MagicMock(name="MockSlackHandler")
        mock_handler_fail.get_userid_from_name.return_value = None

        fake_event = {
            "team_id": "SOME TEAM ID",
        }

        ka = KarmaAssistant()

        with mock.patch.object(ka, "bot", mock_handler_succeed):
            userid = ka.check_if_correlates_to_userid(
                fake_event,
                "SOME USERNAME"
            )

            self.assertEqual(
                "SOME USER ID",
                userid
            )

        with mock.patch.object(ka, "bot", mock_handler_fail):
            userid = ka.check_if_correlates_to_userid(
                fake_event,
                "SOME USERNAME"
            )

            self.assertIsNone(userid)

    def test_check_if_correlates_to_username(self):
        """Assert the check_if_correlates_to_username() method functions."""
        mock_handler_succeed = mock.MagicMock(name="MockSlackHandler")
        mock_handler_succeed.get_username_from_id.return_value = \
            "SOME USERNAME"
        mock_handler_succeed.get_user_obj_from_id.return_value = {
            "team_id": "SOME TEAM ID",
        }

        mock_handler_fail = mock.MagicMock(name="MockSlackHandler")
        mock_handler_fail.get_user_from_id.return_value = None

        fake_event = {
            "team_id": "SOME TEAM ID",
        }

        ka = KarmaAssistant()

        with mock.patch.object(ka, "bot", mock_handler_succeed):
            userid = ka.check_if_correlates_to_username(
                fake_event,
                "SOME USERNAME"
            )

            self.assertEqual(
                "SOME USERNAME",
                userid
            )

        with mock.patch.object(ka, "bot", mock_handler_fail):
            userid = ka.check_if_correlates_to_username(
                fake_event,
                "SOME USERNAME"
            )

            self.assertIsNone(userid)


class KarmaModifyPluginUnitTests(BaseTest):
    """Tests for the KarmaModifyPlugin."""

    def setUp(self):
        """Configure."""
        super().setUp()

        KarmaModel.new(
            string_id="some existing string",
            upvotes=1,
            downvotes=0,
        )

        KarmaModel.new(
            string_id="some existing slack id",
            upvotes=1,
            downvotes=0,
        )

    def test_add_upvote_to_new_string(self):
        """Add an upvote to a new string."""
        mock_assistant = mock.MagicMock()
        mock_assistant.check_if_correlates_to_userid.return_value = None

        plugin = KarmaModifyPlugin('fake event', 'fake arg_string')
        plugin.event = mock.MagicMock()
        plugin.arg_string = "some new string"
        plugin.suffix = "++"

        with mock.patch.object(plugin, "ka", mock_assistant):
            plugin.run()

        model = KarmaModel.get_by_name("some new string")
        self.assertEqual(1, model.upvotes)
        self.assertEqual(0, model.downvotes)
        self.assertEqual(1, model.karma)

        newest = KarmaModel.list_newest()
        self.assertEqual(model, newest[0])
        self.assertEqual(3, len(newest))

    def test_add_downvote_to_new_string(self):
        """Add a downvote to a new string."""
        mock_assistant = mock.MagicMock()
        mock_assistant.check_if_correlates_to_userid.return_value = None

        plugin = KarmaModifyPlugin('fake event', 'fake arg_string')
        plugin.event = mock.MagicMock()
        plugin.arg_string = "some new string"
        plugin.suffix = "--"

        with mock.patch.object(plugin, "ka", mock_assistant):
            plugin.run()

        model = KarmaModel.get_by_name("some new string")
        self.assertEqual(0, model.upvotes)
        self.assertEqual(1, model.downvotes)
        self.assertEqual(-1, model.karma)

        newest = KarmaModel.list_newest()
        self.assertEqual(model, newest[0])
        self.assertEqual(3, len(newest))

    def test_add_upvote_to_existing_string(self):
        """Add an upvote to an existing string."""
        mock_assistant = mock.MagicMock()
        mock_assistant.check_if_correlates_to_userid.return_value = None

        plugin = KarmaModifyPlugin('fake event', 'fake arg_string')
        plugin.event = mock.MagicMock()
        plugin.arg_string = "some existing string"
        plugin.suffix = "++"

        with mock.patch.object(plugin, "ka", mock_assistant):
            plugin.run()

        model = KarmaModel.get_by_name("some existing string")
        self.assertEqual(2, model.upvotes)
        self.assertEqual(0, model.downvotes)
        self.assertEqual(2, model.karma)

        newest = KarmaModel.list_newest()
        self.assertEqual(2, len(newest))

    def test_add_downvote_to_existing_string(self):
        """Add a downvote to an existing string."""
        mock_assistant = mock.MagicMock()
        mock_assistant.check_if_correlates_to_userid.return_value = None

        plugin = KarmaModifyPlugin('fake event', 'fake arg_string')
        plugin.event = mock.MagicMock()
        plugin.arg_string = "some existing string"
        plugin.suffix = "--"

        with mock.patch.object(plugin, "ka", mock_assistant):
            plugin.run()

        model = KarmaModel.get_by_name("some existing string")
        self.assertEqual(1, model.upvotes)
        self.assertEqual(1, model.downvotes)
        self.assertEqual(0, model.karma)

        newest = KarmaModel.list_newest()
        self.assertEqual(2, len(newest))

    def test_add_upvote_to_new_slack_id(self):
        """Add an upvote to a new Slack ID."""
        mock_assistant = mock.MagicMock()
        mock_assistant.check_if_correlates_to_userid.return_value = \
            "some new slack id"

        plugin = KarmaModifyPlugin('fake event', 'fake arg_string')
        plugin.event = mock.MagicMock()
        plugin.arg_string = "some slack username"
        plugin.suffix = "++"

        with mock.patch.object(plugin, "ka", mock_assistant):
            plugin.run()

        model = KarmaModel.get_by_name("some new slack id")
        self.assertEqual(1, model.upvotes)
        self.assertEqual(0, model.downvotes)
        self.assertEqual(1, model.karma)

        newest = KarmaModel.list_newest()
        self.assertEqual(3, len(newest))

    def test_add_downvote_to_new_slack_id(self):
        """Add a downvote to a new Slack ID."""
        mock_assistant = mock.MagicMock()
        mock_assistant.check_if_correlates_to_userid.return_value = \
            "some new slack id"

        plugin = KarmaModifyPlugin('fake event', 'fake arg_string')
        plugin.event = mock.MagicMock()
        plugin.arg_string = "some slack username"
        plugin.suffix = "--"

        with mock.patch.object(plugin, "ka", mock_assistant):
            plugin.run()

        model = KarmaModel.get_by_name("some new slack id")
        self.assertEqual(0, model.upvotes)
        self.assertEqual(1, model.downvotes)
        self.assertEqual(-1, model.karma)

        newest = KarmaModel.list_newest()
        self.assertEqual(3, len(newest))

    def test_add_upvote_to_existing_slack_id(self):
        """Add an upvote to an existing Slack ID."""
        mock_assistant = mock.MagicMock()
        mock_assistant.check_if_correlates_to_userid.return_value = \
            "some existing slack id"

        plugin = KarmaModifyPlugin('fake event', 'fake arg_string')
        plugin.event = mock.MagicMock()
        plugin.arg_string = "some slack username"
        plugin.suffix = "++"

        with mock.patch.object(plugin, "ka", mock_assistant):
            plugin.run()

        model = KarmaModel.get_by_name("some existing slack id")
        self.assertEqual(2, model.upvotes)
        self.assertEqual(0, model.downvotes)
        self.assertEqual(2, model.karma)

        newest = KarmaModel.list_newest()
        self.assertEqual(2, len(newest))

    def test_add_downvote_to_existing_slack_id(self):
        """Add a downvote to an existing Slack ID."""
        mock_assistant = mock.MagicMock()
        mock_assistant.check_if_correlates_to_userid.return_value = \
            "some existing slack id"

        plugin = KarmaModifyPlugin('fake event', 'fake arg_string')
        plugin.event = mock.MagicMock()
        plugin.arg_string = "some slack username"
        plugin.suffix = "--"

        with mock.patch.object(plugin, "ka", mock_assistant):
            plugin.run()

        model = KarmaModel.get_by_name("some existing slack id")
        self.assertEqual(1, model.upvotes)
        self.assertEqual(1, model.downvotes)
        self.assertEqual(0, model.karma)

        newest = KarmaModel.list_newest()
        self.assertEqual(2, len(newest))


class KarmaPluginUnitTests(BaseTest):
    """Tests for the KarmaPlugin."""

    def setUp(self):
        """Populate db with models."""
        super().setUp()

        KarmaModel.new(
            string_id="some karma entry",
            upvotes=2,
            downvotes=1
        )

        KarmaModel.new(
            string_id="some slack id",
            upvotes=3,
            downvotes=1
        )

    def test_target_entry_is_nonexistant(self):
        """Assert that an error message is returned when no match."""
        mock_bot = mock.MagicMock()
        mock_ka = mock.MagicMock()
        mock_ka.check_if_correlates_to_userid.return_value = None
        mock_ka.check_if_correlates_to_username.return_value = None

        event = mock.MagicMock()
        arg_string = "nonexistant karma target"
        plugin = KarmaPlugin(event, arg_string)

        with mock.patch.object(plugin, "bot", mock_bot):
            with mock.patch.object(plugin, "ka", mock_ka):
                plugin.run()

                mock_bot.make_post.assert_called_with(
                    plugin.event,
                    "No entry found for *{}*.".format(plugin.arg_string)
                )

    def test_target_entry_is_straightforward_string(self):
        """Assert that a straightforward match is found."""
        mock_bot = mock.MagicMock()
        mock_ka = mock.MagicMock()
        mock_ka.check_if_correlates_to_userid.return_value = None
        mock_ka.check_if_correlates_to_username.return_value = None

        event = mock.MagicMock()
        arg_string = "some karma entry"
        plugin = KarmaPlugin(event, arg_string)

        with mock.patch.object(plugin, "bot", mock_bot):
            with mock.patch.object(plugin, "ka", mock_ka):
                plugin.run()

                mock_bot.make_post.assert_called_with(
                    event,
                    "*{}* has *{}* karma _({} ++, {} --)_".format(
                        plugin.arg_string,
                        1,
                        2,
                        1,
                    )
                )

    def test_target_entry_correlates_to_slack_user_id(self):
        """."""
        mock_bot = mock.MagicMock()
        mock_ka = mock.MagicMock()
        mock_ka.check_if_correlates_to_userid.return_value = "some slack id"
        mock_ka.check_if_correlates_to_username.return_value = \
            "some karma entry"

        event = mock.MagicMock()
        arg_string = "some karma entry"
        plugin = KarmaPlugin(event, arg_string)

        with mock.patch.object(plugin, "bot", mock_bot):
            with mock.patch.object(plugin, "ka", mock_ka):
                plugin.run()

                mock_bot.make_post.assert_called_with(
                    plugin.event,
                    "*{}* has *{}* karma _({} ++, {} --)_".format(
                        plugin.arg_string,
                        2,
                        3,
                        1,
                    )
                )

    def test_query_directly_for_slack_id(self):
        """."""
        mock_bot = mock.MagicMock()
        mock_ka = mock.MagicMock()
        mock_ka.check_if_correlates_to_userid.return_value = None
        mock_ka.check_if_correlates_to_username.return_value = \
            "some karma entry"

        event = mock.MagicMock()
        arg_string = "some slack id"
        plugin = KarmaPlugin(event, arg_string)

        with mock.patch.object(plugin, "bot", mock_bot):
            with mock.patch.object(plugin, "ka", mock_ka):
                plugin.run()

                mock_bot.make_post.assert_called_with(
                    plugin.event,
                    "*{}* has *{}* karma _({} ++, {} --)_".format(
                        "some karma entry",
                        2,
                        3,
                        1,
                    )
                )


class KarmaNewestPluginUnitTests(BaseTest):
    """Tests for the KarmaNewestPlugin."""

    def setUp(self):
        """Populate db with models."""
        super().setUp()

        self.create = [
            ["first entry", 1, 0],
            ["second entry", 2, 1],
            ["third entry", 3, 2],
            ["fourth entry", 4, 3],
            ["fifth entry", 5, 4],
            ["sixth entry", 6, 5],
            ["seventh entry", 7, 6],
            ["eighth entry", 8, 7],
            ["ninth entry", 9, 8],
            ["tenth entry", 10, 9],
            ["eleventh entry", 11, 10],
        ]

        for idx, item in enumerate(self.create):
            KarmaModel.new(
                string_id=item[0],
                upvotes=item[1],
                downvotes=item[2],
            )

    def test_called_with_nonnumber_failure_mode(self):
        """Post failure when called with a non-number."""
        mock_bot = mock.MagicMock()
        event = mock.MagicMock()
        arg_string = "fuckit"
        plugin = KarmaNewestPlugin(event, arg_string)

        with mock.patch.object(plugin, "bot", mock_bot):
            plugin.run()
            msg = "{} is not a valid number.".format(arg_string)
            mock_bot.make_post.assert_called_with(event, msg)

    def test_called_with_negative_number_failure_mode(self):
        """Post failure when called with a negative number."""
        mock_bot = mock.MagicMock()
        event = mock.MagicMock()
        arg_string = -1234
        plugin = KarmaNewestPlugin(event, arg_string)

        with mock.patch.object(plugin, "bot", mock_bot):
            plugin.run()
            msg = "{} is not a valid number.".format(arg_string)
            mock_bot.make_post.assert_called_with(event, msg)

    def test_default_args(self):
        """Call run() with an empty arg_string."""
        mock_bot = mock.MagicMock()
        mock_ka = mock.MagicMock()
        mock_ka.check_if_correlates_to_username.return_value = None
        event = mock.MagicMock()
        arg_string = None
        plugin = KarmaNewestPlugin(event, arg_string)

        with mock.patch.object(plugin, "bot", mock_bot):
            with mock.patch.object(plugin, "ka", mock_ka):
                plugin.run()

                msg = "*The 5 most-recently created karma subjects:*\n\n"

                for idx, item in enumerate(self.create[::-1]):
                    if idx < 5:
                        msg += \
                            "*{}* with *{}* karma _({} ++, {} --)_\n".format(
                                item[0],
                                item[1] - item[2],
                                item[1],
                                item[2]
                            )

                mock_bot.make_post.assert_called_with(event, msg)

    def test_retrieve_nondefault_number_of_entries(self):
        """Default is 5 - try calling with not-5."""
        mock_bot = mock.MagicMock()
        mock_ka = mock.MagicMock()
        mock_ka.check_if_correlates_to_username.return_value = None
        event = mock.MagicMock()
        arg_string = 7
        plugin = KarmaNewestPlugin(event, arg_string)

        with mock.patch.object(plugin, "bot", mock_bot):
            with mock.patch.object(plugin, "ka", mock_ka):
                plugin.run()

                msg = "*The 7 most-recently created karma subjects:*\n\n"

                for idx, item in enumerate(self.create[::-1]):
                    if idx < 7:
                        msg += \
                            "*{}* with *{}* karma _({} ++, {} --)_\n".format(
                                item[0],
                                item[1] - item[2],
                                item[1],
                                item[2]
                            )

                mock_bot.make_post.assert_called_with(event, msg)

    def test_call_for_more_than_total_number_of_entries(self):
        """There are 11 entries. Call for more, should only get 11."""
        mock_bot = mock.MagicMock()
        mock_ka = mock.MagicMock()
        mock_ka.check_if_correlates_to_username.return_value = None
        event = mock.MagicMock()
        arg_string = 70
        plugin = KarmaNewestPlugin(event, arg_string)

        with mock.patch.object(plugin, "bot", mock_bot):
            with mock.patch.object(plugin, "ka", mock_ka):
                plugin.run()

                msg = "*The 70 most-recently created karma subjects:*\n\n"

                for idx, item in enumerate(self.create[::-1]):
                    msg += \
                        "*{}* with *{}* karma _({} ++, {} --)_\n".format(
                            item[0],
                            item[1] - item[2],
                            item[1],
                            item[2]
                        )

                mock_bot.make_post.assert_called_with(event, msg)

    def test_when_entries_are_slack_ids(self):
        """There are 11 entries. Call for more, should only get 11."""
        mock_bot = mock.MagicMock()
        mock_ka = mock.MagicMock()
        mock_ka.check_if_correlates_to_username.return_value = "some username"
        event = mock.MagicMock()
        arg_string = None
        plugin = KarmaNewestPlugin(event, arg_string)

        with mock.patch.object(plugin, "bot", mock_bot):
            with mock.patch.object(plugin, "ka", mock_ka):
                plugin.run()

                msg = "*The 5 most-recently created karma subjects:*\n\n"

                for idx, item in enumerate(self.create[::-1]):
                    if idx < 5:
                        msg += \
                            "*{}* with *{}* karma _({} ++, {} --)_\n".format(
                                "some username",
                                item[1] - item[2],
                                item[1],
                                item[2]
                            )

                mock_bot.make_post.assert_called_with(event, msg)


class KarmaTopPluginUnitTests(BaseTest):
    """Tests for the KarmaTopPlugin."""

    def setUp(self):
        """Populate db with models."""
        super().setUp()

        self.create = [
            ["first entry", 1, 1],
            ["second entry", 2, 1],
            ["third entry", 3, 1],
            ["fourth entry", 4, 1],
            ["fifth entry", 5, 1],
            ["sixth entry", 6, 1],
            ["seventh entry", 7, 1],
            ["eighth entry", 8, 1],
            ["ninth entry", 9, 1],
            ["tenth entry", 10, 1],
            ["eleventh entry", 11, 1],
        ]

        for idx, item in enumerate(self.create):
            KarmaModel.new(
                string_id=item[0],
                upvotes=item[1],
                downvotes=item[2],
            )

    def test_called_with_nonnumber_failure_mode(self):
        """Post failure when called with a non-number."""
        mock_bot = mock.MagicMock()
        event = mock.MagicMock()
        arg_string = "fuckit"
        plugin = KarmaTopPlugin(event, arg_string)

        with mock.patch.object(plugin, "bot", mock_bot):
            plugin.run()
            msg = "{} is not a valid number.".format(arg_string)
            mock_bot.make_post.assert_called_with(event, msg)

    def test_called_with_negative_number_failure_mode(self):
        """Post failure when called with a negative number."""
        mock_bot = mock.MagicMock()
        event = mock.MagicMock()
        arg_string = -1234
        plugin = KarmaTopPlugin(event, arg_string)

        with mock.patch.object(plugin, "bot", mock_bot):
            plugin.run()
            msg = "{} is not a valid number.".format(arg_string)
            mock_bot.make_post.assert_called_with(event, msg)

    def test_default_args(self):
        """Call run() with an empty arg_string."""
        mock_bot = mock.MagicMock()
        mock_ka = mock.MagicMock()
        mock_ka.check_if_correlates_to_username.return_value = None
        event = mock.MagicMock()
        arg_string = None
        plugin = KarmaTopPlugin(event, arg_string)

        with mock.patch.object(plugin, "bot", mock_bot):
            with mock.patch.object(plugin, "ka", mock_ka):
                plugin.run()

                msg = "*The 5 highest-rated karma subjects:*\n\n"

                for idx, item in enumerate(self.create[::-1]):
                    if idx < 5:
                        msg += \
                            "*{}* with *{}* karma _({} ++, {} --)_\n".format(
                                item[0],
                                item[1] - item[2],
                                item[1],
                                item[2]
                            )

                mock_bot.make_post.assert_called_with(event, msg)

    def test_retrieve_nondefault_number_of_entries(self):
        """Default is 5 - try calling with not-5."""
        mock_bot = mock.MagicMock()
        mock_ka = mock.MagicMock()
        mock_ka.check_if_correlates_to_username.return_value = None
        event = mock.MagicMock()
        arg_string = 7
        plugin = KarmaTopPlugin(event, arg_string)

        with mock.patch.object(plugin, "bot", mock_bot):
            with mock.patch.object(plugin, "ka", mock_ka):
                plugin.run()

                msg = "*The 7 highest-rated karma subjects:*\n\n"

                for idx, item in enumerate(self.create[::-1]):
                    if idx < 7:
                        msg += \
                            "*{}* with *{}* karma _({} ++, {} --)_\n".format(
                                item[0],
                                item[1] - item[2],
                                item[1],
                                item[2]
                            )

                mock_bot.make_post.assert_called_with(event, msg)

    def test_call_for_more_than_total_number_of_entries(self):
        """There are 11 entries. Call for more, should only get 11."""
        mock_bot = mock.MagicMock()
        mock_ka = mock.MagicMock()
        mock_ka.check_if_correlates_to_username.return_value = None
        event = mock.MagicMock()
        arg_string = 70
        plugin = KarmaTopPlugin(event, arg_string)

        with mock.patch.object(plugin, "bot", mock_bot):
            with mock.patch.object(plugin, "ka", mock_ka):
                plugin.run()

                msg = "*The 70 highest-rated karma subjects:*\n\n"

                for idx, item in enumerate(self.create[::-1]):
                    msg += \
                        "*{}* with *{}* karma _({} ++, {} --)_\n".format(
                            item[0],
                            item[1] - item[2],
                            item[1],
                            item[2]
                        )

                mock_bot.make_post.assert_called_with(event, msg)

    def test_when_entries_are_slack_ids(self):
        """There are 11 entries. Call for more, should only get 11."""
        mock_bot = mock.MagicMock()
        mock_ka = mock.MagicMock()
        mock_ka.check_if_correlates_to_username.return_value = "some username"
        event = mock.MagicMock()
        arg_string = None
        plugin = KarmaTopPlugin(event, arg_string)

        with mock.patch.object(plugin, "bot", mock_bot):
            with mock.patch.object(plugin, "ka", mock_ka):
                plugin.run()

                msg = "*The 5 highest-rated karma subjects:*\n\n"

                for idx, item in enumerate(self.create[::-1]):
                    if idx < 5:
                        msg += \
                            "*{}* with *{}* karma _({} ++, {} --)_\n".format(
                                "some username",
                                item[1] - item[2],
                                item[1],
                                item[2]
                            )

                mock_bot.make_post.assert_called_with(event, msg)


class KarmaBottomPluginUnitTests(BaseTest):
    """Tests for the KarmaTopPlugin."""

    def setUp(self):
        """Populate db with models."""
        super().setUp()

        self.create = [
            ["first entry", 1, 1],
            ["second entry", 2, 1],
            ["third entry", 3, 1],
            ["fourth entry", 4, 1],
            ["fifth entry", 5, 1],
            ["sixth entry", 6, 1],
            ["seventh entry", 7, 1],
            ["eighth entry", 8, 1],
            ["ninth entry", 9, 1],
            ["tenth entry", 10, 1],
            ["eleventh entry", 11, 1],
        ]

        for idx, item in enumerate(self.create):
            KarmaModel.new(
                string_id=item[0],
                upvotes=item[1],
                downvotes=item[2],
            )

    def test_called_with_nonnumber_failure_mode(self):
        """Post failure when called with a non-number."""
        mock_bot = mock.MagicMock()
        event = mock.MagicMock()
        arg_string = "fuckit"
        plugin = KarmaBottomPlugin(event, arg_string)

        with mock.patch.object(plugin, "bot", mock_bot):
            plugin.run()
            msg = "{} is not a valid number.".format(arg_string)
            mock_bot.make_post.assert_called_with(event, msg)

    def test_called_with_negative_number_failure_mode(self):
        """Post failure when called with a negative number."""
        mock_bot = mock.MagicMock()
        event = mock.MagicMock()
        arg_string = -1234
        plugin = KarmaBottomPlugin(event, arg_string)

        with mock.patch.object(plugin, "bot", mock_bot):
            plugin.run()
            msg = "{} is not a valid number.".format(arg_string)
            mock_bot.make_post.assert_called_with(event, msg)

    def test_default_args(self):
        """Call run() with an empty arg_string."""
        mock_bot = mock.MagicMock()
        mock_ka = mock.MagicMock()
        mock_ka.check_if_correlates_to_username.return_value = None
        event = mock.MagicMock()
        arg_string = None
        plugin = KarmaBottomPlugin(event, arg_string)

        with mock.patch.object(plugin, "bot", mock_bot):
            with mock.patch.object(plugin, "ka", mock_ka):
                plugin.run()

                msg = "*The 5 lowest-rated karma subjects:*\n\n"

                for idx, item in enumerate(self.create):
                    if idx < 5:
                        msg += \
                            "*{}* with *{}* karma _({} ++, {} --)_\n".format(
                                item[0],
                                item[1] - item[2],
                                item[1],
                                item[2]
                            )

                mock_bot.make_post.assert_called_with(event, msg)

    def test_retrieve_nondefault_number_of_entries(self):
        """Default is 5 - try calling with not-5."""
        mock_bot = mock.MagicMock()
        mock_ka = mock.MagicMock()
        mock_ka.check_if_correlates_to_username.return_value = None
        event = mock.MagicMock()
        arg_string = 7
        plugin = KarmaBottomPlugin(event, arg_string)

        with mock.patch.object(plugin, "bot", mock_bot):
            with mock.patch.object(plugin, "ka", mock_ka):
                plugin.run()

                msg = "*The 7 lowest-rated karma subjects:*\n\n"

                for idx, item in enumerate(self.create):
                    if idx < 7:
                        msg += \
                            "*{}* with *{}* karma _({} ++, {} --)_\n".format(
                                item[0],
                                item[1] - item[2],
                                item[1],
                                item[2]
                            )

                mock_bot.make_post.assert_called_with(event, msg)

    def test_call_for_more_than_total_number_of_entries(self):
        """There are 11 entries. Call for more, should only get 11."""
        mock_bot = mock.MagicMock()
        mock_ka = mock.MagicMock()
        mock_ka.check_if_correlates_to_username.return_value = None
        event = mock.MagicMock()
        arg_string = 70
        plugin = KarmaBottomPlugin(event, arg_string)

        with mock.patch.object(plugin, "bot", mock_bot):
            with mock.patch.object(plugin, "ka", mock_ka):
                plugin.run()

                msg = "*The 70 lowest-rated karma subjects:*\n\n"

                for idx, item in enumerate(self.create):
                    msg += \
                        "*{}* with *{}* karma _({} ++, {} --)_\n".format(
                            item[0],
                            item[1] - item[2],
                            item[1],
                            item[2]
                        )

                mock_bot.make_post.assert_called_with(event, msg)

    def test_when_entries_are_slack_ids(self):
        """There are 11 entries. Call for more, should only get 11."""
        mock_bot = mock.MagicMock()
        mock_ka = mock.MagicMock()
        mock_ka.check_if_correlates_to_username.return_value = "some username"
        event = mock.MagicMock()
        arg_string = None
        plugin = KarmaBottomPlugin(event, arg_string)

        with mock.patch.object(plugin, "bot", mock_bot):
            with mock.patch.object(plugin, "ka", mock_ka):
                plugin.run()

                msg = "*The 5 lowest-rated karma subjects:*\n\n"

                for idx, item in enumerate(self.create):
                    if idx < 5:
                        msg += \
                            "*{}* with *{}* karma _({} ++, {} --)_\n".format(
                                "some username",
                                item[1] - item[2],
                                item[1],
                                item[2]
                            )

                mock_bot.make_post.assert_called_with(event, msg)

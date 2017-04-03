from dungeonbot.conftest import BaseTest
from dungeonbot.plugins.attribute import AttrPlugin
from dungeonbot.models.attribute import AttrModel
from datetime import datetime
from unittest import mock


class AttributeTests(BaseTest):
    """Setup for Attribute tests."""

    def setUp(self):
        """Set up Attribute Model Tests."""
        super().setUp()
        self.user = {"id": "U1N796T52", "name": "phil"}
        self.user2 = {"id": "U1N796T51", "name": "sara"}

        self.mock_event = {
            "text": "",
            "type": "message",
            "user": self.user,
            "ts": "1472164181.000061",
            "channel": "C2377T63B",
            "event_ts": "1472164181.000061",
            "team_id": "T1N7FEJHE",
        }
        self.plugin = AttrPlugin(self.mock_event, self.user)
        self.model = AttrModel()

        self.model.set(args=["macademia", 4], user=self.user)
        self.model.set(args=["hazelnut", 7], user=self.user2)


class AttributeModelTests(AttributeTests):
    """Tests the Attribute Model."""

    def test_new_model_has_base_attrs(self):
        """Test that a newly-instantiated attribute has minimum attributes."""
        columns = ["id", "key", "val", "user", "created"]
        for column in columns:
            assert hasattr(self.model, column)

    def test_model_can_be_added(self):
        """Assert that AttrModel can be added to db."""
        attr = AttrModel()
        attr.key = "TestKey"
        attr.val = "TestVal"
        attr.user = self.user["id"]
        attr.created = datetime.utcnow()

        self.db.session.add(attr)
        self.db.session.commit()

        assert attr in self.db.session

    def test_set_successful(self):
        """Assert that set successfully adds an attribute to db."""
        args = ["walnut", 13]
        m = self.model.set(args, self.user)
        assert m in self.db.session

    def test_set_invalid(self):
        """Assert that set will not add an inproperly formatted key/val."""
        num_before = len(self.model.list(user=self.user))
        args = ["cashew"]
        m = self.model.set(args, self.user)
        assert m is None
        assert num_before == len(self.model.list(user=self.user))

    def test_set_duplicate(self):
        """Assert that attempting to add a duplicate key will not add, and will return None."""
        args = ["peanut", 10]
        m1 = self.model.set(args, self.user)
        num_before = len(self.model.list(user=self.user))
        m2 = self.model.set(args, self.user)
        assert m1 in self.db.session
        assert m2 is "duplicate"
        assert num_before == len(self.model.list(user=self.user))

    def test_get_successful(self):
        """Assert that key can be retrieved with get."""
        instance = self.model.get("macademia", self.user)
        assert instance and instance.key == "macademia" and instance.val == "4"

    def test_get_another_user_key(self):
        """Assert that a user cannot retrieve another user's keys."""
        assert self.model.get(args="hazelnut", user=self.user) is None
        assert self.model.get(args="macademia", user=self.user2) is None
        assert self.model.get(args="hazelnut", user=self.user2)
        assert self.model.get(args="macademia", user=self.user)

    def test_get_failed(self):
        """Assert that attempting to get nonexistant key will return None."""
        assert self.model.get("almond", self.user) is None

    def test_list(self):
        """Assert that list will return keys."""
        # import pdb; pdb.set_trace()
        userlist = self.model.list(user=self.user2)
        assert len(userlist) == 1
        self.model.set(["brazil", 42], self.user2)
        assert len(self.model.list(user=self.user2)) == 2

    def test_delete_success(self):
        """Assert that delete will remove from db and return string."""
        m = self.model.set(["brazil", 42], self.user2)
        assert m in self.db.session
        assert self.model.get(m.key, self.user2)
        m_delete = self.model.delete(args=m.key, user=self.user2)
        assert m_delete == m.key
        assert self.model.get(m.key, self.user2) is None

    def test_delete_nonexistant_key(self):
        """Assert deleting nonexistant key returns None."""
        len_before = len(self.model.list(user=self.user2))
        assert self.model.delete("pineapple", self.user2) is None
        assert len_before == len(self.model.list(user=self.user2))

    def test_delete_key_not_owned_by_you(self):
        """Assert that user cannot delete another user's key."""
        d = self.model.delete("hazelnut", self.user)
        assert d is None
        assert self.model.get("hazelnut", self.user2)


class AttributePluginTests(AttributeTests):
    """Tests the Attribute Plugin."""

    def test_run(self):
        """Assert that AttrPlugin runs."""
        mock_parser = mock.Mock(name="process_attr")
        mock_parser.return_value = "Success"

        evt = self.mock_event
        arg = "get strength"
        with mock.patch.object(AttrPlugin, 'process_attr', mock_parser):
            handler = AttrPlugin(evt, arg)
            handler.run()

            self.assertTrue(mock_parser.called)

    def test_process_attr_invalid_command(self):
        """Assert that invalid commands are handled properly by process attr."""
        args = "ketchup"
        assert self.plugin.process_attr(args, self.user) == "Not a valid command."

    def test_process_attr_get(self):
        """Assert that process attr handles get command."""
        mock_parser = mock.Mock(name="get_key")
        mock_parser.return_value = "Success"

        evt = self.mock_event
        arg = "get strength"
        with mock.patch.object(AttrPlugin, 'get_key', mock_parser):
            handler = AttrPlugin(evt, arg)
            handler.process_attr(arg.split(), self.user)

            self.assertTrue(mock_parser.called)

    def test_process_attr_set(self):
        """Assert that process attr handles set command."""
        mock_parser = mock.Mock(name="set_key")
        mock_parser.return_value = "Success"

        evt = self.mock_event
        arg = "set strength 4"
        with mock.patch.object(AttrPlugin, 'set_key', mock_parser):
            handler = AttrPlugin(evt, arg)
            handler.process_attr(arg.split(), self.user)

            self.assertTrue(mock_parser.called)

    def test_process_attr_list(self):
        """Assert that process attr handles list command."""
        mock_parser = mock.Mock(name="list_keys")
        mock_parser.return_value = "Success"

        evt = self.mock_event
        arg = "list"
        with mock.patch.object(AttrPlugin, 'list_keys', mock_parser):
            handler = AttrPlugin(evt, arg)
            handler.process_attr(arg.split(), self.user)

            self.assertTrue(mock_parser.called)

    def test_process_attr_delete(self):
        """Assert that process attr handles delete command."""
        mock_parser = mock.Mock(name="delete_key")
        mock_parser.return_value = "Success"

        evt = self.mock_event
        arg = "delete rutabaga "
        with mock.patch.object(AttrPlugin, 'delete_key', mock_parser):
            handler = AttrPlugin(evt, arg)
            handler.process_attr(arg.split(), self.user)

            self.assertTrue(mock_parser.called)

    def test_get_key_not_in_db(self):
        """Test retrieving a non-existant key from db."""
        arg = ["battle-ax"]
        assert self.plugin.get_key(arg, self.user) == "Could not find {}".format(arg)

    def test_get_existing_key(self):
        """Test that we can retrieve an existing key from db."""
        args = ["pistachio", 12]
        self.model.set(args, self.user)
        assert self.plugin.get_key(args[:1], self.user) == "{}: {}".format(*args)

    def test_set_key_duplicate(self):
        """Assert that duplicate key cannot be saved and appropriate message returned."""
        args = ["hazelnut", 2]
        assert self.plugin.set_key(args, self.user2) == "You already have a key with that name."

    def test_set_key_success(self):
        """Assert that key/val can be successfully set."""
        args = ["watermelon", 24]
        assert self.plugin.set_key(args, self.user) == "Saved:\n{}: {}".format(*args)
        assert self.model.get(args[0], self.user)

    def test_set_key_failure_one_arg(self):
        """Assert that passing in only a key will return correct error message."""
        args = ["pineapple"]
        assert self.plugin.set_key(args, self.user) == "Could not save key."

    def test_set_key_failure_no_arg(self):
        """Assert that passing in no args will return correct error message."""
        args = []
        assert self.plugin.set_key(args, self.user) == "Could not save key."

    def test_list_keys_no_items(self):
        """Assert listing keys for user with no keys looks as expected."""
        user3 = {"id": "U3834953", "name": "selena"}
        assert self.plugin.list_keys([], user3) == "Listing attributes for {}".format(user3["name"])

    def test_list_keys(self):
        """Assert listing keys for user is properly formatted."""
        message = "Listing attributes for {}\n{}: {}".format(self.user["name"], "macademia", 4)
        assert self.plugin.list_keys([], self.user) == message
        self.plugin.set_key(["carrots", 2], self.user)
        assert self.plugin.list_keys([], self.user) == message + "\ncarrots: 2"

    def test_delete_key_successful(self):
        """Assert that delete keys returns proper message."""
        assert self.plugin.delete_key(["hazelnut"], self.user2) == "Successfully deleted hazelnut"
        assert not self.model.get("hazelnut", self.user2)

    def test_delete_key_failure(self):
        """Assert that attempting to delete nonexistant key returns proper message."""
        assert not self.model.get("chocolate", self.user)
        assert self.plugin.delete_key(["chocolate"], self.user) == "Could not delete key."

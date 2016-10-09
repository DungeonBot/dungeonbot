from dungeonbot.conftest import BaseTest
from dungeonbot.plugins.roll import RollPlugin
from dungeonbot.models.roll import RollModel
from datetime import datetime


class RollModelTest(BaseTest):
    """Extended off of Basetest to test the Roll Model."""

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
        self.plugin = RollPlugin(self.mock_event, self.user)
        self.model = RollModel
        self.model.new("sword", "1d6", self.user)
        self.model.new("axe", "1d12", self.user)

    def test_new_model_has_base_attrs(self):
        """Test that a newly-instantiated roll object has minimum attributes."""
        columns = ["id", "key", "val", "user", "created"]
        for column in columns:
            assert hasattr(self.model, column)

    def test_model_can_be_added(self):
        """Assert that RollModel can be added to db."""
        roll = RollModel()
        roll.key = "TestKey"
        roll.val = "7d40"
        roll.user = self.user["id"]
        roll.created = datetime.utcnow()

        self.db.session.add(roll)
        self.db.session.commit()

        assert roll in self.db.session

    def test_new_successful(self):
        """Assert that new successfully adds a roll to db."""
        args = ["bow", "1d6"]
        m = self.model.new(args[0], args[1], self.user)
        instance = self.model.get(m.key, self.user)
        assert instance.key == "bow" and instance.val == "1d6"

    def test_new_invalid(self):
        """Assert that new will not add an inproperly formatted key/val."""
        num_before = len(self.model.list(user=self.user))
        args = ["harpsicode"]
        m = self.model.new(args[0], [], self.user)
        assert m is None
        assert num_before == len(self.model.list(user=self.user))

    def test_set_duplicate(self):
        """Assert that attempting to add a duplicate key will not add, and will return None."""
        args = ["rustyshovel", "2d6"]
        m1 = self.model.new(args[0], args[1], self.user)
        num_before = len(self.model.list(user=self.user))
        m2 = self.model.new(args[0], args[1], self.user)
        assert m1 in self.db.session
        assert m2 is "duplicate"
        assert num_before == len(self.model.list(user=self.user))

    def test_get_successful(self):
        """Assert that key can be retrieved with get."""
        one = self.model.get("sword", self.user)
        two = self.model.get("axe", self.user)
        self.assertEqual(one.key, "sword")
        self.assertEqual(one.val, "1d6")
        self.assertEqual(two.key, "axe")
        self.assertEqual(two.val, "1d12")

    def test_get_another_user_key(self):
        """Assert that a user cannot retrieve another user's keys."""
        assert self.model.get(key="sword", user=self.user2) is None
        assert self.model.get(key="sword", user=self.user)

    def test_get_failed(self):
        """Assert that attempting to get nonexistant key will return None."""
        assert self.model.get("fish", self.user) is None
        assert self.model.get("uke", self.user) is None

    def test_list(self):
        """Assert that list will return keys."""
        userlist = self.model.list(user=self.user)
        assert len(userlist) == 2
        self.model.new("wrench", "1d4", self.user)
        assert len(self.model.list(user=self.user)) == 3

    def test_delete_success(self):
        """Assert that delete will remove from db and return string."""
        m = self.model.new("words", "1d10", self.user)
        assert m in self.db.session
        assert self.model.get(m.key, self.user)
        m_delete = self.model.delete(m)
        assert m_delete == m.key
        assert not self.model.get(m.key, self.user)

    def test_delete_nonexistant_key(self):
        """Assert deleting nonexistant key returns None."""
        len_before = len(self.model.list(user=self.user))
        assert self.model.delete("pineapple", self.user) is None
        assert len_before == len(self.model.list(user=self.user))

    def test_slack_msg(self):
        """Assert slack_msg looks as expected."""
        m = self.model.get("sword", self.user)
        assert m.slack_msg == "sword: 1d6"

    def test_json(self):
        """Assert json representation looks as expected."""
        m = self.model.get("sword", self.user)
        expected = {
            "id": m.id,
            "key": m.key,
            "value": m.val,
            "user": m.user
        }
        assert m.json == expected

    def test_repr(self):
        inst = self.model.get("sword", self.user)
        message = """
            <dungeonbot.models.RollModel(id={},key={}, value={}, user={})>
            """.format(inst.id, inst.key, inst.val, inst.user)
        assert inst.__str__() == message

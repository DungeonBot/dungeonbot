from dungeonbot.conftest import BaseTest

from dungeonbot.models.quest import QuestModel

from datetime import datetime


class QuestUnitTests(BaseTest):
    """Class for testing quests"""

    def test_new_model_has_base_attrs(self):
        """Test that a newly-instantiated quest has minimum attributes."""
        quest = QuestModel()
        attrs = ["id", "title", "description", "status", "created"]
        for attr in attrs:
            assert hasattr(quest, attr)

    def test_create_new_quest_manual_add(self):
        """Test that a new quest can be added to the database."""
        quest = QuestModel()
        quest.title = "Test quest"
        quest.created = datetime.utcnow()
        quest.last_updated = datetime.utcnow()

        self.db.session.add(quest)
        self.db.session.commit()

        assert quest in self.db.session

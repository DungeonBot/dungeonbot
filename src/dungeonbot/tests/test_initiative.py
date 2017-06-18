from dungeonbot.conftest import BaseTest
from dungeonbot.plugins.initiative import InitiativePlugin
from dungeonbot.models.initiative import InitiativeModel
from datetime import datetime
from unittest.mock import Mock, patch


class InitiativeModelUnitTests(BaseTest):
    """Test the Initiative model."""

    def setUp(self):
        super().setUp()

        self.model = InitiativeModel()
        self.model.set(name="Goblins", init=6)
        self.model.set(name="Kobolds", init=9)

    def test_new_model_has_base_attrs(self):
        """A newly-instantiated initiative entity should have minimum attributes."""
        columns = ["id", "name", "init", "created"]
        for column in columns:
            assert hasattr(self.model, column)

    def test_model_can_be_added(self):
        """Assert that InitiativeModel can be added to the db."""
        instance = InitiativeModel(name="Beholder", init=30, created=datetime.utcnow())

        self.db.session.add(instance)
        self.db.session.commit()

        assert instance in self.db.session

    def test_set_success(self):
        """Assert that '.set' successfully adds a single entity to the db."""
        instance = self.model.set(name="Tanarukk", init=22)

        assert instance in self.db.session

    def test_set_duplicate(self):
        """Assert that '.set' will not add an entity that shares a name with an existing one."""
        i1 = self.model.set(name="Behir", init=17)
        num_instances = len(self.model.list())
        i2 = self.model.set(name="Behir", init=14)

        assert i1 in self.db.session
        assert i2 == "duplicate"
        assert num_instances == len(self.model.list())

    def test_get_success(self):
        """Assert that '.get' successfully retrieves a single entity."""
        entity = self.model.get(name="Kobolds")

        assert entity and entity.name == "Kobolds" and entity.init == 9

    def test_get_failure(self):
        """Assert that '.get' will return None when looking for nonexistant entity name."""
        assert self.model.get(name="A high elf that isn't haughty") is None

    def test_delete_success(self):
        """Assert that '.delete' will remove an entity from the db."""
        num_instances_before = len(self.model.list())
        entity = self.model.delete(name="Goblins")

        assert num_instances_before > len(self.model.list())
        assert entity not in self.db.session

    def test_delete_failure(self):
        """Assert that '.delete' will return None when looking for nonexistant entity name."""
        assert self.model.delete(name="Francis McEmptyButt") is None

    def test_list(self):
        """Assert that '.list' returns every entity in the initiative list."""
        entities = self.model.list()

        assert len(entities) == 2
        for entity in entities:
            assert entity.name in ["Goblins", "Kobolds"]

    def test_clear(self):
        """Assert that '.clear' removes all entities from the initiative list."""
        self.model.clear()
        
        assert len(self.model.list()) == 0


class InitiativePluginUnitTests(BaseTest):
    """Test the Initiative plugin."""

    def setUp(self):
        """Set up Initiative Model tests."""
        super().setUp()

        self.model = InitiativeModel
        self.model.set(name="Flumph", init=12)
        self.model.set(name="Flameskull", init=13)

    def test_run_invalid_subcommand(self):
        """Assert that '.run' handles invalid subcommands properly."""
        mock_event = Mock()
        arg_string="invalid_subcommand"

        plugin = InitiativePlugin(event=mock_event, arg_string=arg_string)

        mock_bot = Mock()
        with patch.object(plugin, "bot", mock_bot):
            plugin.run()

        mock_bot.make_post.assert_called_with(
            mock_event,
            f"'{arg_string}': Not a valid !init subcommand."
        )

    def test_run_valid_subcommand(self):
        """Assert that '.run' handles valid subcommands properly."""
        mock_event = Mock()
        arg_string = "get"

        plugin = InitiativePlugin(mock_event, arg_string)

        mock_bot = Mock()
        mock_get_entity = Mock(return_value="success")
        with patch.multiple(plugin, bot=mock_bot, get_entity=mock_get_entity):
            plugin.run()

        mock_get_entity.assert_called()
        mock_bot.make_post.assert_called_with(mock_event, "success")

    def test_get_single_entity_success(self):
        """Assert that '.get_entity' succeeds for a single valid entity."""
        mock_event = Mock()
        arg_string = "get Flameskull"
        expected_message = (
            "*Initiative Query Results:*"
            "\nFlameskull: 13"
        )
        
        plugin = InitiativePlugin(mock_event, arg_string)

        mock_bot = Mock()
        with patch.object(plugin, "bot", mock_bot):
            plugin.run()

        mock_bot.make_post.assert_called_with(
            mock_event,
            expected_message,
        )

    def test_get_single_entity_failure(self):
        """Assert that '.get_entity' supplies a proper single-entity failure message."""
        mock_event = Mock()
        arg_string = "get Bailey"
        expected_message = (
            "*Initiative Query Results:*"
            "\nBailey: Not Found"
        )

        plugin = InitiativePlugin(mock_event, arg_string)

        mock_bot = Mock()
        with patch.object(plugin, "bot", mock_bot):
            plugin.run()

        mock_bot.make_post.assert_called_with(
            mock_event,
            expected_message,
        )
    
    def test_get_multiple_entities_success(self):
        """Assert that '.get_entity' succeeds for several valid entries."""
        mock_event = Mock()
        arg_string = "get Flameskull, Flumph"
        expected_message = (
            "*Initiative Query Results:*"
            "\nFlameskull: 13"
            "\nFlumph: 12"
        )

        plugin = InitiativePlugin(mock_event, arg_string)

        mock_bot = Mock()
        with patch.object(plugin, "bot", mock_bot):
            plugin.run()

        mock_bot.make_post.assert_called_with(
            mock_event,
            expected_message,
        )

    def test_get_multiple_entities_failure(self):
        """Assert that '.get_entity' handles multiple failures."""
        mock_event = Mock()
        arg_string = "get Bailey, Zane"
        expected_message = (
            "*Initiative Query Results:*"
            "\nBailey: Not Found"
            "\nZane: Not Found"
        )

        plugin = InitiativePlugin(mock_event, arg_string)

        mock_bot = Mock()
        with patch.object(plugin, "bot", mock_bot):
            plugin.run()

        mock_bot.make_post.assert_called_with(
            mock_event,
            expected_message,
        )

    def test_get_multiple_entities_mixed_success(self):
        """Assert that '.get_entity' handles multiple successes and failures."""
        mock_event = Mock()
        arg_string = "get Flameskull, Bailey, Flumph, Zane"
        expected_message = (
            "*Initiative Query Results:*"
            "\nFlameskull: 13"
            "\nBailey: Not Found"
            "\nFlumph: 12"
            "\nZane: Not Found"
        )

        plugin = InitiativePlugin(mock_event, arg_string)

        mock_bot = Mock()
        with patch.object(plugin, "bot", mock_bot):
            plugin.run()

        mock_bot.make_post.assert_called_with(
            mock_event,
            expected_message,
        )

    def test_add_single_entity_success_via_value(self):
        """Assert that a valid 'NAME VALUE' can be added."""
        mock_event = Mock()
        arg_string = "add Jackalwere 12"
        expected_message = (
            "Entity (or entities) added."
        )

        plugin = InitiativePlugin(mock_event, arg_string)

        mock_bot = Mock()
        with patch.object(plugin, "bot", mock_bot):
            plugin.run()

        mock_bot.make_post.assert_called_with(
            mock_event,
            expected_message,
        )
    
    def test_add_single_entity_failure_value_not_given(self):
        """Assert that a missing VALUE fails properly."""
        mock_event = Mock()
        arg_string = "add Jackalwere"
        expected_message = (
            "Errors:"
            "\n'Jackalwere': Value not given or not an integer."
            "\n\nOther entries not mentioned should have worked."
        )

        plugin = InitiativePlugin(mock_event, arg_string)

        mock_bot = Mock()
        with patch.object(plugin, "bot", mock_bot):
            plugin.run()

        assert InitiativeModel.get(name="Jackalwere") is None
        mock_bot.make_post.assert_called_with(
            mock_event,
            expected_message,
        )

    def test_add_single_entity_failure_non_integer_value(self):
        """Assert that a non-integer VALUE fails properly."""
        mock_event = Mock()
        arg_string = "add Jackalwere twelve"
        expected_message = (
            "Errors:"
            "\n'Jackalwere twelve': Value not given or not an integer."
            "\n\nOther entries not mentioned should have worked."
        )

        plugin = InitiativePlugin(mock_event, arg_string)

        mock_bot = Mock()
        with patch.object(plugin, "bot", mock_bot):
            plugin.run()

        assert InitiativeModel.get(name="Jackalwere") is None
        mock_bot.make_post.assert_called_with(
            mock_event,
            expected_message,
        )

    def test_add_single_entity_failure_duplicate_value(self):
        """Assert that adding a duplicate NAME fails properly."""
        mock_event = Mock()
        arg_string = "add Flumph 17"
        expected_message = (
            "Errors:"
            "\n'Flumph 17': Duplicate entity name."
            "\n\nOther entries not mentioned should have worked."
        )

        plugin = InitiativePlugin(mock_event, arg_string)

        mock_bot = Mock()
        with patch.object(plugin, "bot", mock_bot):
            plugin.run()

        assert InitiativeModel.get(name="Flumph").init == 12
        mock_bot.make_post.assert_called_with(
            mock_event,
            expected_message,
        )

    def test_add_single_entity_success_flat_roll(self):
        """Assert that a valid 'NAME -r' can be added."""
        mock_event = Mock()
        arg_string = "add Goristro -r"
        expected_message = (
            "Entity (or entities) added."
        )

        plugin = InitiativePlugin(mock_event, arg_string)

        mock_bot = Mock()
        with patch.object(plugin, "bot", mock_bot):
            plugin.run()

        entity = InitiativeModel.get(name="Goristro")
        assert entity
        assert 1 <= entity.init <= 20
        mock_bot.make_post.assert_called_with(
            mock_event,
            expected_message,
        )
    
    def test_add_single_entity_failure_flat_roll_duplicate(self):
        """Assert that 'NAME -r' doesn't add an entity with a duplicate 'NAME'."""
        mock_event = Mock()
        arg_string = "add Flumph -r"
        expected_message = (
            "Errors:"
            "\n'Flumph -r': Duplicate entity name."
            "\n\nOther entries not mentioned should have worked."
        )

        plugin = InitiativePlugin(mock_event, arg_string)

        mock_bot = Mock()
        with patch.object(plugin, "bot", mock_bot):
            plugin.run()

        assert InitiativeModel.get(name="Flumph").init == 12
        mock_bot.make_post.assert_called_with(
            mock_event,
            expected_message,
        )

    def test_add_single_entity_success_mod_roll(self):
        """Assert that a valid 'NAME -r MOD' can be added."""
        mock_event = Mock()
        arg_string = "add Cloaker -r +2"
        expected_message = (
            "Entity (or entities) added."
        )

        plugin = InitiativePlugin(mock_event, arg_string)

        mock_bot = Mock()
        with patch.object(plugin, "bot", mock_bot):
            plugin.run()

        entity = InitiativeModel.get(name="Cloaker")
        assert entity is not None
        assert 3 <= entity.init <= 23
        mock_bot.make_post.assert_called_with(
            mock_event,
            expected_message,
        )

    def test_add_single_entity_failure_non_integer_mod_roll(self):
        """Assert that 'NAME -r MOD' fails properly on an invalid 'MOD'."""
        mock_event = Mock()
        arg_string = "add Cloaker -r +two"
        expected_message = (
            "Errors:"
            "\n'Cloaker -r +two': Modifier must be a positive or negative integer."
            "\n\nOther entries not mentioned should have worked."
        )

        plugin = InitiativePlugin(mock_event, arg_string)

        mock_bot = Mock()
        with patch.object(plugin, "bot", mock_bot):
            plugin.run()

        assert InitiativeModel.get(name="Cloaker") is None
        mock_bot.make_post.assert_called_with(
            mock_event,
            expected_message,
        )

    def test_add_single_entity_failure_duplicate_mod_roll(self):
        """Assert that 'NAME -r MOD' fails properly on duplicate 'NAME'."""
        mock_event = Mock()
        arg_string = "add Flameskull -r +3"
        expected_message = (
            "Errors:"
            "\n'Flameskull -r +3': Duplicate entity name."
            "\n\nOther entries not mentioned should have worked."
        )

        plugin = InitiativePlugin(mock_event, arg_string)

        mock_bot = Mock()
        with patch.object(plugin, "bot", mock_bot):
            plugin.run()

        entity = InitiativeModel.get(name="Flameskull")
        assert entity is not None
        assert entity.init == 13
        mock_bot.make_post.assert_called_with(
            mock_event,
            expected_message,
        )

    def test_add_multiple_entities_success(self):
        """Assert multiple entites of mixed formats can be added."""
        mock_event = Mock()
        arg_string = "add Chuul 7, Dragon Turtle -r, Ghost -r +1, Mummy -r -1"
        expected_message = (
            "Entity (or entities) added."
        )

        plugin = InitiativePlugin(mock_event, arg_string)

        mock_bot = Mock()
        with patch.object(plugin, "bot", mock_bot):
            plugin.run()

        assert len(InitiativeModel.list()) == 6
        assert InitiativeModel.get(name="Chuul").init == 7
        assert 1 <= InitiativeModel.get(name="Dragon Turtle").init <= 20
        assert 2 <= InitiativeModel.get(name="Ghost").init <= 21
        assert 0 <= InitiativeModel.get(name="Mummy").init <= 19
        mock_bot.make_post.assert_called_with(
            mock_event,
            expected_message,
        )

    def test_add_multiple_entities_partial_success(self):
        """Assert multiple entities of mixed formats and varying success can be added."""
        mock_event = Mock()
        arg_string = "add Rakshasa -r +3, Flameskull -r, Quaggoth nine, Camel 18, Roc"
        expected_message = (
            "Errors:"
            "\n'Flameskull -r': Duplicate entity name."
            "\n'Quaggoth nine': Value not given or not an integer."
            "\n'Roc': Value not given or not an integer."
            "\n\nOther entries not mentioned should have worked."
        )

        plugin = InitiativePlugin(mock_event, arg_string)

        mock_bot = Mock()
        with patch.object(plugin, "bot", mock_bot):
            plugin.run()

        assert len(InitiativeModel.list()) == 4
        assert 4 <= InitiativeModel.get(name="Rakshasa").init <= 23
        assert InitiativeModel.get(name="Camel").init == 18
        mock_bot.make_post.assert_called_with(
            mock_event,
            expected_message,
        )

    def test_remove_single_entity_success(self):
        """Assert that a single entity can be deleted."""
        mock_event = Mock()
        arg_string = "remove Flumph"
        expected_message = "Done."

        plugin = InitiativePlugin(mock_event, arg_string)

        mock_bot = Mock()
        with patch.object(plugin, "bot", mock_bot):
            plugin.run()

        assert len(InitiativeModel.list()) == 1
        assert InitiativeModel.get(name="Flumph") is None
        mock_bot.make_post.assert_called_with(
            mock_event,
            expected_message,
        )

    def test_remove_single_entity_failure(self):
        """Assert that trying to remove a nonexistant entity fails silently."""
        mock_event = Mock()
        arg_string = "remove Yeti"
        expected_message = "Done."

        plugin = InitiativePlugin(mock_event, arg_string)

        mock_bot = Mock()
        with patch.object(plugin, "bot", mock_bot):
            plugin.run()

        assert len(InitiativeModel.list()) == 2
        mock_bot.make_post.assert_called_with(
            mock_event,
            expected_message,
        )

    def test_remove_multiple_entities_success(self):
        """Assert that multiple entites can be removed together."""
        mock_event = Mock()
        arg_string = "remove Flumph, Flameskull"
        expected_message = "Done."

        plugin = InitiativePlugin(mock_event, arg_string)

        mock_bot = Mock()
        with patch.object(plugin, "bot", mock_bot):
            plugin.run()

        assert len(InitiativeModel.list()) == 0
        assert InitiativeModel.get(name="Flameskull") is None
        assert InitiativeModel.get(name="Flumph") is None
        mock_bot.make_post.assert_called_with(
            mock_event,
            expected_message,
        )

    def test_remove_multiple_entities_failure(self):
        """Assert that multiple entities can be removed, including nonexistant 'failures'."""
        mock_event = Mock()
        arg_string = "remove Flumph, Sahuagin, Owlbear, Flameskull"
        expected_message = "Done."

        plugin = InitiativePlugin(mock_event, arg_string)

        mock_bot = Mock()
        with patch.object(plugin, "bot", mock_bot):
            plugin.run()

        assert len(InitiativeModel.list()) == 0
        assert InitiativeModel.get(name="Flameskull") is None
        assert InitiativeModel.get(name="Flumph") is None
        mock_bot.make_post.assert_called_with(
            mock_event,
            expected_message,
        )

    def test_list_entities(self):
        """Assert that all entities are listed."""
        mock_event = Mock()
        arg_string = "list"
        expected_message = (
            "*Current Initiative:*"
            "\n> _*13*_ -- Flameskull"
            "\n> _*12*_ -- Flumph"
        )

        plugin = InitiativePlugin(mock_event, arg_string)

        mock_bot = Mock()
        with patch.object(plugin, "bot", mock_bot):
            plugin.run()

        mock_bot.make_post.assert_called_with(
            mock_event,
            expected_message,
        )

    def test_clear_entities(self):
        """Assert that all entities are deleted."""
        mock_event = Mock()
        arg_string = "clear"
        expected_message = (
            "Initiative cleared."
        )

        plugin = InitiativePlugin(mock_event, arg_string)

        mock_bot = Mock()
        with patch.object(plugin, "bot", mock_bot):
            plugin.run()

        assert len(InitiativeModel.list()) == 0
        assert InitiativeModel.get("Flumph") is None
        assert InitiativeModel.get("Flameskull") is None
        mock_bot.make_post.assert_called_with(
            mock_event,
            expected_message,
        )


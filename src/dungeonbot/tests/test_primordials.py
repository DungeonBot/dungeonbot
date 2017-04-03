"""Test plugin parent classes."""


from dungeonbot.conftest import BaseTest

from dungeonbot.plugins.primordials import (
    BasePlugin,
    SlackEnabledPlugin,
    BangCommandPlugin,
    SuffixCommandPlugin,
)

from unittest import mock


class BasePluginUnitTests(BaseTest):
    """Test the BasePlugin parent class."""

    def test_base_plugin_configuration(self):
        """Assert that the BasePlugin functinos properly."""
        plugin = BasePlugin()

        self.assertEqual(
            plugin.help_text,
            "Somebody didn't give their plugin any help text. For shame."
        )


class SlackEnabledPluginUnitTests(BaseTest):
    """Test the SlackEnabledPlugin parent class."""

    def test_slack_enabled_plugin_configuration(self):
        """Assert that the SlackEnabledPlugin functions properly."""
        base_plugin = BasePlugin()
        mock_event = mock.MagicMock()
        plugin = SlackEnabledPlugin(mock_event)

        mock_bot = mock.MagicMock()

        with mock.patch.object(plugin, "bot", mock_bot):
            plugin.help()

            self.assertEqual(
                base_plugin.help_text,
                plugin.help_text
            )

            mock_bot.make_post.assert_called_with(
                mock_event,
                base_plugin.help_text
            )


class BangCommandPluginUnitTests(BaseTest):
    """Test the BangCommandPlugin parent class."""

    def test_bang_command_plugin_configuration(self):
        """Assert that the BangCommandPlugin functions properly."""
        mock_event = mock.MagicMock()
        arg_string = "literally fucking anything at this point"
        plugin = BangCommandPlugin(mock_event, arg_string)

        self.assertIsNotNone(plugin.help_text)
        self.assertIsNotNone(plugin.help)
        self.assertIsNotNone(plugin.arg_string)


class SuffixCommandPluginUnitTests(BaseTest):
    """Test the SuffixCommandPlugin parent class."""

    def test_suffix_command_plugin_configuration(self):
        """Assert that the SuffixCommandPlugin functions properly."""
        mock_event = mock.MagicMock()
        arg_string = "literally fucking anything at this point"
        suffix = "fuckit"
        plugin = SuffixCommandPlugin(mock_event, arg_string, suffix)

        self.assertIsNotNone(plugin.help_text)
        self.assertIsNotNone(plugin.help)
        self.assertIsNotNone(plugin.arg_string)
        self.assertIsNotNone(plugin.suffix)

"""Tests for the help plugin."""


from dungeonbot.conftest import BaseTest

from dungeonbot.plugins.help import HelpPlugin

from unittest import mock


class HelpPluginUnitTests(BaseTest):
    """Test the help plugin."""

    def test_help_topic_exists(self):
        """Ensure that the topic dict works."""
        event = mock.MagicMock()
        arg_string = "test_key"
        plugin = HelpPlugin(event, arg_string)

        mock_external_plugin = mock.MagicMock()
        topics_dict = {'test_key': mock_external_plugin}

        with mock.patch.object(plugin, "help_topics", topics_dict):
            plugin.run()

            self.assertTrue(mock_external_plugin.called)
            mock_external_plugin.assert_called_with(event, arg_string)

    def test_help_topic_doesnt_exist(self):
        """Ensure that HelpPlugin's own help function runs."""
        event = mock.MagicMock()
        arg_string = ""
        plugin = HelpPlugin(event, arg_string)

        mock_external_plugin = mock.MagicMock()
        mock_help_method = mock.MagicMock()
        topics_dict = {'test_key': mock_external_plugin}

        with mock.patch.object(plugin, "help_topics", topics_dict):
            with mock.patch.object(plugin, "help", mock_help_method):
                plugin.run()

                self.assertFalse(mock_external_plugin.called)
                self.assertTrue(mock_help_method.called)

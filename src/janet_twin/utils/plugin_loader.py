# File: plugin_loader.py
from src.janet_twin.orchestrator.registry import PluginRegistry
from plugins.echo_plugin import EchoPlugin
from plugins.base_plugins import GoogleSearchPlugin, LogsSearch
from plugins.conversation_plugin import ConversationPlugin

def register_plugins(registry: PluginRegistry):
    """
    Registers all available plugins with the given registry.

    :param registry: The PluginRegistry instance to register plugins with.
    """
    registry.register("echo", EchoPlugin())
    registry.register("search", GoogleSearchPlugin())
    registry.register("conversation", ConversationPlugin())
    registry.register("logsearch", LogsSearch())
    registry.register("logs", LogsSearch())
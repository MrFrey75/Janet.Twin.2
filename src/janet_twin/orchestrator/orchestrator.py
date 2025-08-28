from src.janet_twin.models.task import Task
from .registry import PluginRegistry
from src.janet_twin.utils.logger_utility import logger
from src.janet_twin.utils.conversation_utility import ConversationUtility


class Orchestrator:
    def __init__(self, registry: PluginRegistry):
        self.registry = registry

    def handle(self, task: Task):
        logger.info(f"Orchestrator received: {task.command}")

        plugin = self.registry.get(task.command)
        if not plugin:
            logger.warning(f"No plugin found for {task.command}")
            return f"Sorry, I don’t know how to handle '{task.command}' yet."

        try:
            result = plugin.execute(task.payload or {})
            logger.debug(f"Task {task.command} executed successfully")
            return result
        except Exception as e:
            logger.error(f"Plugin {task.command} failed: {e}")
            return f"Error running {task.command}: {str(e)}"
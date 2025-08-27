import os
import yaml
from src.janet_twin.utils.logger_utility import logger

CONVERSATION_PATH = os.path.join("data", "conversations")

class ConversationUtility:
    def __init__(self):
        if not os.path.exists(CONVERSATION_PATH):
            os.makedirs(CONVERSATION_PATH)
            logger.info(f"Conversation directory created at {CONVERSATION_PATH}")

    @staticmethod
    def save_conversation(unique_id: str, conversation_data: dict):
        """Save a conversation to a new YAML file."""
        filename = f"{unique_id}.yaml"
        filepath = os.path.join(CONVERSATION_PATH, filename)
        try:
            with open(filepath, "w") as f:
                yaml.dump(conversation_data, f)
            logger.info(f"Conversation with UUID {unique_id} saved to {filepath}.")
        except Exception as e:
            logger.error(f"Error saving conversation {unique_id}: {e}")

    @staticmethod
    def load_conversation(unique_id: str):
        """Load a conversation from its YAML file."""
        filename = f"{unique_id}.yaml"
        filepath = os.path.join(CONVERSATION_PATH, filename)
        if os.path.exists(filepath):
            try:
                with open(filepath, "r") as f:
                    conversation_data = yaml.safe_load(f)
                    return conversation_data
            except Exception as e:
                logger.error(f"Error loading conversation {unique_id}: {e}")
        return None

    @staticmethod
    def delete_conversation(self, unique_id: str):
        """Delete a conversation's YAML file."""
        filename = f"{unique_id}.yaml"
        filepath = os.path.join(CONVERSATION_PATH, filename)
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                logger.info(f"Conversation file {filepath} deleted.")
            except Exception as e:
                logger.error(f"Error deleting conversation {unique_id}: {e}")

    @staticmethod
    def get_conversation_dict():
        """Get a dictionary of all conversation files in the data/conversations directory."""
        conversation_list = []

        conversation_dict = {}
        for filename in os.listdir(CONVERSATION_PATH):
            if not filename.endswith(".yaml"):
                continue
            with open(os.path.join(CONVERSATION_PATH, filename), "r") as f:
                data = yaml.safe_load(f)

            if not data:
                ConversationUtility.delete_conversation(filename)
                continue

            conversation_dict["title"] = data.get("title", "Untitled")
            conversation_dict["filename"] = filename
            conversation_dict["last_update"] = data.get("last_update", "")

        return conversation_dict
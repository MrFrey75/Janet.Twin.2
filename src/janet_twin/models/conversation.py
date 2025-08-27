from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
from typing import Any, Dict

@dataclass
class Conversation:
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)
    unique_id: UUID = field(default_factory=uuid4)
    filename: str = ""
    title: str = ""
    messages: list[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Converts the Conversation object to a dictionary for saving."""
        return {
            "unique_id": str(self.unique_id),
            "created_at": self.created_at.isoformat(),
            "last_updated": self.last_updated.isoformat(),
            "filename": self.filename,
            "title": self.title,
            "messages": self.messages
        }

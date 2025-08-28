from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class Task:
    user: str
    command: str
    intent: str = None
    payload: Dict[str, Any] = None

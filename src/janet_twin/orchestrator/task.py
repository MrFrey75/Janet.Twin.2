from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class Task:
    user: str
    command: str
    payload: Dict[str, Any] = None

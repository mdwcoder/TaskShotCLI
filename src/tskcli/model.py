from dataclasses import dataclass, asdict
from typing import Optional
from datetime import datetime

@dataclass
class Task:
    id: int
    text: str
    status: str = "pending"  # pending, done
    priority: Optional[str] = None  # low, med, high
    due: Optional[str] = None  # YYYY-MM-DD
    created_at: str = ""
    done_at: Optional[str] = None

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(data):
        return Task(**data)

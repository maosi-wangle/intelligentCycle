from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Deque
from uuid import uuid4

from app.core.config import settings


@dataclass
class MemoryTurn:
    role: str
    content: str


class ConversationMemory:
    def __init__(self, window_size: int) -> None:
        self.window_size = window_size
        self._store: dict[str, Deque[MemoryTurn]] = defaultdict(lambda: deque(maxlen=window_size))

    def new_conversation_id(self) -> str:
        return uuid4().hex

    def append(self, conversation_id: str, role: str, content: str) -> None:
        self._store[conversation_id].append(MemoryTurn(role=role, content=content))

    def history(self, conversation_id: str) -> list[MemoryTurn]:
        return list(self._store.get(conversation_id, deque(maxlen=self.window_size)))

    def clear(self, conversation_id: str) -> None:
        self._store.pop(conversation_id, None)


conversation_memory = ConversationMemory(settings.ai_memory_window)

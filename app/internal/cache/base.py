from abc import ABC, abstractmethod
from typing import Any, Optional
import hashlib


class Cache(ABC):
    @staticmethod
    def make_key(s: Any) -> str:
        return hashlib.sha1(str(s).encode()).hexdigest()

    @abstractmethod
    def dump_result(
        self, data: Any, key: str, screenshot: Optional[bytes] = None
    ) -> None:
        pass

    @abstractmethod
    def load_result(self, key: str) -> Optional[Any]:
        pass

    @abstractmethod
    def screenshot_location(self, key: str) -> str:
        pass

import os
import json
from pathlib import Path
from typing import Any, Optional

from settings import USER_DATA_DIR, SCREENSHOT_TYPE
from .base import Cache


class FileSystemCache(Cache):
    def __init__(self, base_dir: Path = USER_DATA_DIR):
        self.base_dir = base_dir

    def dump_result(
        self, data: Any, key: str, screenshot: Optional[bytes] = None
    ) -> None:
        path = self._json_location(key)

        # create dir if not exists
        d = os.path.dirname(path)
        if not os.path.exists(d):
            os.makedirs(d, exist_ok=True)

        # save result as json
        with open(path, mode="w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=True)

        # save screenshot
        if screenshot:
            with open(self._screenshot_location(key), mode="wb") as f:
                f.write(screenshot)

    def load_result(self, key: str) -> Optional[Any]:
        path = self._json_location(key)
        if not path.exists():
            return None
        with open(path, mode="r", encoding="utf-8") as f:
            return json.load(f)

    def _json_location(self, filename: str) -> Path:
        return self.base_dir / "_res" / filename[:2] / filename

    def _screenshot_location(self, filename: str) -> Path:
        return (
            self.base_dir / "_res" / filename[:2] / (filename + "." + SCREENSHOT_TYPE)
        )

    def screenshot_location(self, key: str) -> Path:
        return self.base_dir / "_res" / key[:2] / (key + "." + SCREENSHOT_TYPE)

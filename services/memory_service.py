import json
from pathlib import Path
from typing import Any, Dict, Optional


class MemoryService:
    """
    Very simple JSON file-based storage for long-term memory.
    """

    def __init__(self, base_dir: str = "data") -> None:
        self.base_path = Path(base_dir)
        self.base_path.mkdir(exist_ok=True)

    def _file_path(self, filename: str) -> Path:
        return self.base_path / filename

    def load_json(self, filename: str) -> Optional[Dict[str, Any]]:
        path = self._file_path(filename)
        if not path.exists():
            return None
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def save_json(self, filename: str, data: Dict[str, Any]) -> None:
        path = self._file_path(filename)
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

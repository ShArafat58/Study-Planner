from datetime import datetime
from typing import Any


class LoggingService:
    """
    Minimal logging service. In a real system this might integrate with
    structured logging or observability tools.
    """

    def log(self, source: str, message: str, data: Any | None = None) -> None:
        timestamp = datetime.now().isoformat(timespec="seconds")
        line = f"[{timestamp}] [{source}] {message}"
        if data is not None:
            line += f" | {data}"
        print(line)

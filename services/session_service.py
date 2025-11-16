from typing import Any, Dict


class SessionService:
    """
    Simple in-memory session store.
    In a real system this could be replaced with Redis or a database.
    """

    def __init__(self) -> None:
        self._state: Dict[str, Any] = {}

    def get(self, key: str, default: Any = None) -> Any:
        return self._state.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._state[key] = value

    def all(self) -> Dict[str, Any]:
        return dict(self._state)

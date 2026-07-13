from __future__ import annotations

from dataclasses import dataclass
from typing import Any


EXIT_INTERNAL = 1
EXIT_VALIDATION = 2
EXIT_HLEDGER_DISCOVERY = 3
EXIT_HLEDGER_EXECUTION = 4
EXIT_OUTPUT = 5


@dataclass(slots=True)
class AdapterError(Exception):
    code: str
    message: str
    exit_code: int = EXIT_VALIDATION
    detail: dict[str, Any] | None = None

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"

    def to_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "status": "error",
            "error": {
                "code": self.code,
                "message": self.message,
            },
        }
        if self.detail:
            payload["error"]["detail"] = self.detail
        return payload


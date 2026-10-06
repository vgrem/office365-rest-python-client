from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class Report(ClientValue):
    """Returns the content appropriate for the context

    Args:
        content (str): Report content; details vary by report type.
    """

    content: bytes | None = None

    def to_bytes(self) -> bytes:
        """Returns the report content as bytes (``b""`` when empty)."""
        return self.content or b""

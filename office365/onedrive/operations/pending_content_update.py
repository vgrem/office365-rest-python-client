from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class PendingContentUpdate(ClientValue):
    """Indicates that an operation that might affect the binary content of the driveItem is pending completion."""

    queuedDateTime: str | None = None

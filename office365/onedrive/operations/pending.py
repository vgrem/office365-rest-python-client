from __future__ import annotations

from dataclasses import dataclass, field

from office365.onedrive.operations.pending_content_update import PendingContentUpdate
from office365.runtime.client_value import ClientValue


@dataclass
class PendingOperations(ClientValue):
    """Indicates that one or more operations that might affect the state of the driveItem are pending completion."""

    pendingContentUpdate: PendingContentUpdate | None = field(default_factory=PendingContentUpdate)

from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class PendingContentUpdate(ClientValue):
    """Indicates that an operation that might affect the binary content of the driveItem is pending completion."""

    queuedDateTime: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PendingContentUpdate"

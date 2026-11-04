from __future__ import annotations

from datetime import time

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class WindowsUpdateActiveHoursInstall(ClientValue):
    activeHoursEnd: time | None = None
    activeHoursStart: time | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsUpdateActiveHoursInstall"

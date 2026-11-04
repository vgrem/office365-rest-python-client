from __future__ import annotations

from datetime import datetime

from office365.intune.devices.management.managed.actionstate import ActionState
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class DeviceActionResult(ClientValue):
    actionName: str | None = None
    actionState: ActionState = ActionState.none
    lastUpdatedDateTime: datetime | None = None
    startDateTime: datetime | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceActionResult"

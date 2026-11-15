from __future__ import annotations

from office365.security.alerts.actions.device import DeviceAction
from office365.security.alerts.states.isolation_type import IsolationType


class IsolateDeviceAction(DeviceAction):
    isolationType: IsolationType = IsolationType.full

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.IsolateDeviceAction"

from __future__ import annotations

from office365.security.device_action import DeviceAction
from office365.security.isolation_type import IsolationType


class IsolateDeviceAction(DeviceAction):
    isolationType: IsolationType = IsolationType.full

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.IsolateDeviceAction"

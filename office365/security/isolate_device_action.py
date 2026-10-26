from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue
from office365.security.isolation_type import IsolationType


@dataclass
class IsolateDeviceAction(ClientValue):
    isolationType: IsolationType = IsolationType.full

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.IsolateDeviceAction"

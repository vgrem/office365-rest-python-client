from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class IosDeviceType(ClientValue):
    iPad: bool | None = None
    iPhoneAndIPod: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.IosDeviceType"

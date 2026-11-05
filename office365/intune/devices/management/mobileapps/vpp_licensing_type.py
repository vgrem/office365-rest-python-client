from __future__ import annotations

from office365.runtime.client_value import ClientValue


class VppLicensingType(ClientValue):
    supportsDeviceLicensing: bool | None = None
    supportsUserLicensing: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.VppLicensingType"

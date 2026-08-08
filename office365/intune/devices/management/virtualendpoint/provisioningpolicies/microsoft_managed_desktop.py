from __future__ import annotations

from dataclasses import dataclass

from office365.intune.devices.management.virtualendpoint.provisioningpolicies.microsoftmanageddesktoptype import (
    MicrosoftManagedDesktopType,
)
from office365.runtime.client_value import ClientValue


@dataclass
class MicrosoftManagedDesktop(ClientValue):
    managedType: MicrosoftManagedDesktopType = MicrosoftManagedDesktopType.notManaged
    profile: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MicrosoftManagedDesktop"

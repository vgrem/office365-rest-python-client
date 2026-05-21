from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from office365.runtime.client_value import ClientValue


@dataclass
class SPContainerApplicationProperties(ClientValue):
    ContainerTypeId: UUID | None = None
    IsGovernableByAdmin: bool | None = None
    OwningApplicationId: UUID | None = None
    OwningApplicationName: str | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPContainerApplicationProperties"

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from office365.runtime.client_value import ClientValue


@dataclass
class SPContainerTypeStatus(ClientValue):
    ContainerTypeId: UUID | None = None
    IsActiveBillingProfile: bool | None = None
    IsArchivable: bool | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPContainerTypeStatus"

from __future__ import annotations

from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class SPContainerTypeStatus(ClientValue):
    ContainerTypeId: UUID | None = None
    IsActiveBillingProfile: bool | None = None
    IsArchivable: bool | None = None
    BillingClassification: int | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPContainerTypeStatus"

from uuid import UUID

from office365.runtime.client_value import ClientValue
from typing import Optional


class SPContainerTypeStatus(ClientValue):
    def __init__(
        self,
        container_type_id: Optional[UUID] = None,
        is_active_billing_profile: Optional[bool] = None,
        is_archivable: Optional[bool] = None,
    ):
        self.ContainerTypeId = container_type_id
        self.IsActiveBillingProfile = is_active_billing_profile
        self.IsArchivable = is_archivable

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPContainerTypeStatus"

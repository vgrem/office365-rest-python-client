from typing import Optional
from uuid import UUID

from office365.runtime.client_value import ClientValue


class SPContainerApplicationProperties(ClientValue):
    def __init__(
        self,
        container_type_id: Optional[UUID] = None,
        is_governable_by_admin: Optional[bool] = None,
        owning_application_id: Optional[UUID] = None,
        owning_application_name: Optional[str] = None,
    ):
        self.ContainerTypeId = container_type_id
        self.IsGovernableByAdmin = is_governable_by_admin
        self.OwningApplicationId = owning_application_id
        self.OwningApplicationName = owning_application_name

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPContainerApplicationProperties"

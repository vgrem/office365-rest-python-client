from uuid import UUID

from office365.runtime.client_value import ClientValue
from typing import Optional


class SPDeletedContainerTypeProperties(ClientValue):
    def __init__(self, container_type_id: Optional[UUID] = None):
        self.ContainerTypeId = container_type_id

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPDeletedContainerTypeProperties"

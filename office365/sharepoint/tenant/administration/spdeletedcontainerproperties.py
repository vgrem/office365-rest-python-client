from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


class SPDeletedContainerProperties(ClientValue):
    def __init__(
        self,
        container_id: Optional[str] = None,
        container_name: Optional[str] = None,
        created_on: Optional[datetime] = None,
        deleted_on: Optional[datetime] = None,
    ):
        self.ContainerId = container_id
        self.ContainerName = container_name
        self.CreatedOn = created_on
        self.DeletedOn = deleted_on

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPDeletedContainerProperties"

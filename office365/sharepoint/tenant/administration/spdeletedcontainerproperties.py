from datetime import datetime

from office365.runtime.client_value import ClientValue


class SPDeletedContainerProperties(ClientValue):
    def __init__(
        self,
        container_id: str = None,
        container_name: str = None,
        created_on: datetime = None,
        deleted_on: datetime = None,
    ):
        self.ContainerId = container_id
        self.ContainerName = container_name
        self.CreatedOn = created_on
        self.DeletedOn = deleted_on

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPDeletedContainerProperties"

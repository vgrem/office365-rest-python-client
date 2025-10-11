from uuid import UUID

from office365.runtime.client_value import ClientValue


class SPDeletedContainerTypeProperties(ClientValue):

    def __init__(self, container_type_id: UUID = None):
        self.ContainerTypeId = container_type_id

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPDeletedContainerTypeProperties"

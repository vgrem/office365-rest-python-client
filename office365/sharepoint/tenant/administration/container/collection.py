from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.tenant.administration.container.properties import (
    SPContainerProperties,
)


class SPContainerCollection(ClientValue):
    def __init__(
        self,
        container_collection: ClientValueCollection[SPContainerProperties] = ClientValueCollection(
            SPContainerProperties
        ),
        paging_token: str = None,
    ):
        self.ContainerCollection = container_collection
        self.PagingToken = paging_token

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPContainerCollection"

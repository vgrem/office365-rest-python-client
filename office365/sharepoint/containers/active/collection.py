from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.containers.active.properties import (
    SPActiveContainerProperties,
)


class SPActiveContainerCollection(ClientValue):
    def __init__(
        self,
        container_collection: ClientValueCollection[SPActiveContainerProperties] = ClientValueCollection(
            SPActiveContainerProperties
        ),
        paging_token: str = None,
    ):
        self.ContainerCollection = container_collection
        self.PagingToken = paging_token

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Containers.SPActiveContainerCollection"

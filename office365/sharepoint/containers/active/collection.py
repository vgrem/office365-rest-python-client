from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.containers.active.properties import (
    SPActiveContainerProperties,
)


@dataclass
class SPActiveContainerCollection(ClientValue):
    ContainerCollection: ClientValueCollection[SPActiveContainerProperties] = field(
        default_factory=lambda: ClientValueCollection(SPActiveContainerProperties)
    )
    PagingToken: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Containers.SPActiveContainerCollection"

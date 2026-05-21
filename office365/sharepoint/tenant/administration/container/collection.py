from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.tenant.administration.container.properties import (
    SPContainerProperties,
)


@dataclass
class SPContainerCollection(ClientValue):
    ContainerCollection: ClientValueCollection[SPContainerProperties] = field(
        default_factory=lambda: ClientValueCollection(SPContainerProperties)
    )
    PagingToken: str | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPContainerCollection"

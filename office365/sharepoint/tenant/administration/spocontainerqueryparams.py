from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.tenant.administration.container.filterorder import (
    SPContainerFilterOrder,
)
from office365.sharepoint.tenant.administration.container.sortorder import (
    SPContainerSortOrder,
)


@dataclass
class SPOContainerQueryParams(ClientValue):
    FilterByColumnsList: ClientValueCollection[SPContainerFilterOrder] = field(
        default_factory=lambda: ClientValueCollection(SPContainerFilterOrder)
    )
    OrderByColumnsList: ClientValueCollection[SPContainerSortOrder] = field(
        default_factory=lambda: ClientValueCollection(SPContainerSortOrder)
    )
    PagingToken: str | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOContainerQueryParams"

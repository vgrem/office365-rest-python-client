from __future__ import annotations

from dataclasses import field
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


class ListOfIdsProviderParameters(ClientValue):
    ListId: UUID | None = None
    ListItemIds: ClientValueCollection = field(default_factory=ClientValueCollection)

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.SiteManager.ListOfIdsProviderParameters"

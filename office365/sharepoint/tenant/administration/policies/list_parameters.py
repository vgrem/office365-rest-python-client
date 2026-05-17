from typing import Optional
from uuid import UUID

from office365.runtime.client_value import ClientValue


class SPOListParameters(ClientValue):
    def __init__(self, id_: Optional[UUID] = None, title: Optional[str] = None):
        self.Id = id_
        self.Title = title

    ""

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOListParameters"

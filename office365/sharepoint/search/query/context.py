from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import GuidCollection, StringCollection


@dataclass
class QueryContext(ClientValue):
    """This object contains the query context properties."""

    GroupObjectIds: StringCollection = field(default_factory=StringCollection)
    SpSiteId: str | None = None
    TenantInstanceId: str | None = None
    PortalUrl: str | None = None
    RoleIds: GuidCollection = field(default_factory=GuidCollection)
    SpWebId: str | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.QueryContext"

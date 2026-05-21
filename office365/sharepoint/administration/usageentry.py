from __future__ import annotations

from typing import Optional


from dataclasses import dataclass
from office365.runtime.client_value import ClientValue


@dataclass
class UsageEntry(ClientValue):

    EventTypeId: Optional[int] = None
    ItemId: Optional[str] = None
    ScopeId: Optional[str] = None
    Site: Optional[str] = None
    User: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.UsageEntry"
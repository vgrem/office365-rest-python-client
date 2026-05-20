from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class ParentGroup(ClientValue):
    DisplayName: Optional[str] = None
    GroupSiteUrl: Optional[str] = None
    ID: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.ParentGroup"

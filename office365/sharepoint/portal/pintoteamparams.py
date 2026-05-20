from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.portal.m365tabitem import M365TabItem


@dataclass
class PinToTeamParams(ClientValue):
    tabs: ClientValueCollection[M365TabItem] = field(default_factory=lambda: ClientValueCollection(M365TabItem))
    teamsId: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.PinToTeamParams"

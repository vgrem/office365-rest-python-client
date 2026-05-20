from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class ChannelInfo(ClientValue):
    description: Optional[str] = None
    displayName: Optional[str] = None
    filesFolderWebUrl: Optional[str] = None
    id: Optional[str] = None
    memberShipType: Optional[int] = None
    webUrl: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.ChannelInfo"

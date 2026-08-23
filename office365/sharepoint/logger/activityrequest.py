from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class LogActivityRequest(ClientValue):
    LastAccessTime: Optional[str] = None
    ListItemUniqueId: Optional[str] = None
    IsAdjusted: bool | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Internal.LogActivityRequest"

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class ActivityClientResponse(ClientValue):
    id: str
    message: Optional[str] = None
    serverId: Optional[str] = None
    status: Optional[int] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Activities.ActivityClientResponse"

from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue


class ActivityClientResponse(ClientValue):
    id: str
    message: Optional[str] = None
    serverId: Optional[str] = None
    status: Optional[int] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Activities.ActivityClientResponse"

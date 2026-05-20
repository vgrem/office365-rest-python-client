from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class ActivityCapabilities(ClientValue):
    clientActivitiesEnabled: Optional[bool] = None
    clientActivitiesNotificationEnabled: Optional[bool] = None
    enabled: Optional[bool] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Activities.ActivityCapabilities"

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional


from dataclasses import dataclass
from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class SubscriptionInformation(ClientValue):

    """Parameter class for webhook Update and Create REST operations."""

    notificationUrl
    resource
    expirationDateTime: Optional[datetime] = None
    clientState: Optional[str] = None
    resourceData: Optional[str] = None
    scenarios: StringCollection = StringCollection()

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Webhooks.SubscriptionInformation"
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class SubscriptionInformation(ClientValue):
    """Parameter class for webhook Update and Create REST operations."""

    notificationUrl: Optional[str] = None
    resource: Optional[str] = None
    expirationDateTime: Optional[datetime] = None
    clientState: Optional[str] = None
    resourceData: Optional[str] = None
    scenarios: StringCollection = field(default_factory=StringCollection)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Webhooks.SubscriptionInformation"

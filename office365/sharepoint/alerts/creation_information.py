from __future__ import annotations

from datetime import datetime
from typing import Optional


from dataclasses import dataclass
from office365.runtime.client_value import ClientValue


@dataclass
class AlertCreationInformation(ClientValue):

    """An object that contain the properties used to create a new SP.Alert"""

    AlertFrequency: Optional[int] = None
    AlertTemplateName: Optional[str] = None
    AlertType: Optional[int] = None
    AlertTime: datetime = datetime.min
    AlwaysNotify: Optional[bool] = None
    DeliveryChannels: Optional[int] = None
    EventType: Optional[int] = None
    EventTypeBitmask: Optional[int] = None
    Filter: Optional[str] = None
    Properties: Optional[dict] = None
    Status: Optional[int] = None
    Title: Optional[str] = None
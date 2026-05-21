from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.publishing.calltoaction import CallToAction as _CallToAction
from office365.sharepoint.publishing.icon import Icon as _Icon


@dataclass
class AnnouncementsData(ClientValue):
    CallToAction: _CallToAction = field(default_factory=lambda: _CallToAction())
    Dismissable: Optional[bool] = None
    ExpiresOn: Optional[datetime] = None
    Icon: _Icon = field(default_factory=lambda: _Icon())
    ID: Optional[str] = None
    Message: Optional[str] = None
    PublishStartDate: Optional[datetime] = None
    Title: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.AnnouncementsData"

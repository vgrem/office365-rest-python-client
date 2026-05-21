from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class ApprovalRequestCreationInfo(ClientValue):
    Approvers: StringCollection = field(default_factory=StringCollection)
    AwaitAll: Optional[bool] = None
    DistributionChannel: StringCollection = field(default_factory=StringCollection)
    Important: Optional[bool] = None
    Message: Optional[str] = None
    PublishOption: Optional[str] = None
    SchedulePublishDate: Optional[datetime] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.ApprovalRequestCreationInfo"

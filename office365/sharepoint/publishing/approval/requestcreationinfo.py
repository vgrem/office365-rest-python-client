from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class ApprovalRequestCreationInfo(ClientValue):
    def __init__(
        self,
        approvers: StringCollection = StringCollection(),
        await_all: Optional[bool] = None,
        distribution_channel: StringCollection = StringCollection(),
        important: Optional[bool] = None,
        message: Optional[str] = None,
        publish_option: Optional[str] = None,
        schedule_publish_date: Optional[datetime] = None,
    ):
        self.Approvers = approvers
        self.AwaitAll = await_all
        self.DistributionChannel = distribution_channel
        self.Important = important
        self.Message = message
        self.PublishOption = publish_option
        self.SchedulePublishDate = schedule_publish_date

    @property
    def entity_type_name(self):
        return "SP.Publishing.ApprovalRequestCreationInfo"

from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection
from typing import Optional


class MMTaskSettings(ClientValue):
    def __init__(
        self,
        agent_group_name: Optional[str] = None,
        scheduled_time_utc: Optional[datetime] = None,
        scheduled_type: Optional[int] = None,
        tags: Optional[StringCollection] = None,
    ):
        self.AgentGroupName = agent_group_name
        self.ScheduledTimeUtc = scheduled_time_utc
        self.ScheduledType = scheduled_type
        self.Tags = tags

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MigrationCenter.Common.MMTaskSettings"

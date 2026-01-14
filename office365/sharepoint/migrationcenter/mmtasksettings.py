from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class MMTaskSettings(ClientValue):
    def __init__(
        self,
        agent_group_name: str = None,
        scheduled_time_utc: datetime = None,
        scheduled_type: int = None,
        tags: StringCollection = None,
    ):
        self.AgentGroupName = agent_group_name
        self.ScheduledTimeUtc = scheduled_time_utc
        self.ScheduledType = scheduled_type
        self.Tags = tags

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MigrationCenter.Common.MMTaskSettings"

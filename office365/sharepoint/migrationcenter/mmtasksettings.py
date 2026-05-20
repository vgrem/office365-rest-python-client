from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class MMTaskSettings(ClientValue):
    AgentGroupName: Optional[str] = None
    ScheduledTimeUtc: Optional[datetime] = None
    ScheduledType: Optional[int] = None
    Tags: Optional[StringCollection] = None

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MigrationCenter.Common.MMTaskSettings"

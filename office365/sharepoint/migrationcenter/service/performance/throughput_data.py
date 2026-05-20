from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class ThroughputData(ClientValue):
    Bytes: Optional[int] = None
    EndTime: Optional[datetime] = None
    Files: Optional[int] = None
    StartTime: Optional[datetime] = None

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MigrationCenter.Service.ThroughputData"

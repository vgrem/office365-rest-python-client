from datetime import datetime

from office365.runtime.client_value import ClientValue
from typing import Optional


class ThroughputData(ClientValue):
    def __init__(
        self,
        bytes_: Optional[int] = None,
        end_time: Optional[datetime] = None,
        files: Optional[int] = None,
        start_time: Optional[datetime] = None,
    ):
        self.Bytes = bytes_
        self.EndTime = end_time
        self.Files = files
        self.StartTime = start_time

    ""

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MigrationCenter.Service.ThroughputData"

from datetime import datetime

from office365.runtime.client_value import ClientValue
from typing import Optional


class MigrationProperty(ClientValue):
    def __init__(
        self, key: Optional[str] = None, updated_time_utc: Optional[datetime] = None, value: Optional[str] = None
    ):
        self.key = key
        self.updatedTimeUtc = updated_time_utc
        self.value = value

    ""

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MigrationCenter.Service.MigrationProperty"

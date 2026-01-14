from datetime import datetime

from office365.runtime.client_value import ClientValue


class MigrationProperty(ClientValue):
    def __init__(self, key: str = None, updated_time_utc: datetime = None, value: str = None):
        self.key = key
        self.updatedTimeUtc = updated_time_utc
        self.value = value

    ""

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MigrationCenter.Service.MigrationProperty"

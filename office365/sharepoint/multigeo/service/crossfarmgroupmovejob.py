from datetime import datetime
from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class CrossFarmGroupMoveJob(Entity):
    @odata(name="IsContentMoved")
    @property
    def is_content_moved(self) -> Optional[bool]:
        """Gets the IsContentMoved property"""
        return self.properties.get("IsContentMoved", None)

    @odata(name="LastModified")
    @property
    def last_modified(self) -> datetime:
        """Gets the LastModified property"""
        return self.properties.get("LastModified", datetime.min)

    @odata(name="StartedDateInUtc")
    @property
    def started_date_in_utc(self) -> datetime:
        """Gets the StartedDateInUtc property"""
        return self.properties.get("StartedDateInUtc", datetime.min)

    @odata(name="StateName")
    @property
    def state_name(self) -> Optional[str]:
        """Gets the StateName property"""
        return self.properties.get("StateName", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.CrossFarmGroupMoveJob"

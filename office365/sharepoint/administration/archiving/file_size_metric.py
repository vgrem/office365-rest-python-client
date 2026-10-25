from datetime import datetime
from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class ArchiveFileSizeMetric(Entity):
    """ """

    @odata(name="ActiveStorageInGB")
    @property
    def active_storage_in_gb(self) -> Optional[float]:
        """Gets the ActiveStorageInGB property"""
        return self.properties.get("ActiveStorageInGB", None)

    @odata(name="ArchivedStorageInGB")
    @property
    def archived_storage_in_gb(self) -> Optional[float]:
        """Gets the ArchivedStorageInGB property"""
        return self.properties.get("ArchivedStorageInGB", None)

    @odata(name="InactiveStorageInGB")
    @property
    def inactive_storage_in_gb(self) -> Optional[float]:
        """Gets the InactiveStorageInGB property"""
        return self.properties.get("InactiveStorageInGB", None)

    @odata(name="LastRefreshOn")
    @property
    def last_refresh_on(self) -> Optional[datetime]:
        """Gets the LastRefreshOn property"""
        return self.properties.get("LastRefreshOn", None)

    @odata(name="UnsupportedStorageInGB")
    @property
    def unsupported_storage_in_gb(self) -> Optional[float]:
        """Gets the UnsupportedStorageInGB property"""
        return self.properties.get("UnsupportedStorageInGB", None)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.Archiving.ArchiveFileSizeMetric"

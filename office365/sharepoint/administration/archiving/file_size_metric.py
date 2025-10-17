from datetime import datetime
from typing import Optional

from office365.sharepoint.entity import Entity


class ArchiveFileSizeMetric(Entity):
    """ """

    @property
    def active_storage_in_gb(self) -> Optional[float]:
        """Gets the ActiveStorageInGB property"""
        return self.properties.get("ActiveStorageInGB", None)

    @property
    def archived_storage_in_gb(self) -> Optional[float]:
        """Gets the ArchivedStorageInGB property"""
        return self.properties.get("ArchivedStorageInGB", None)

    @property
    def inactive_storage_in_gb(self) -> Optional[float]:
        """Gets the InactiveStorageInGB property"""
        return self.properties.get("InactiveStorageInGB", None)

    @property
    def last_refresh_on(self) -> datetime:
        """Gets the LastRefreshOn property"""
        return self.properties.get("LastRefreshOn", None)

    @property
    def unsupported_storage_in_gb(self) -> Optional[float]:
        """Gets the UnsupportedStorageInGB property"""
        return self.properties.get("UnsupportedStorageInGB", None)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.Archiving.ArchiveFileSizeMetric"

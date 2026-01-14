from datetime import datetime
from typing import Optional
from uuid import UUID

from office365.sharepoint.entity import Entity


class DeletedSiteProperties(Entity):
    @property
    def archive_status(self) -> Optional[str]:
        """Gets the ArchiveStatus property"""
        return self.properties.get("ArchiveStatus", None)

    @property
    def days_remaining(self) -> Optional[int]:
        """Gets the DaysRemaining property"""
        return self.properties.get("DaysRemaining", None)

    @property
    def deletion_time(self) -> datetime:
        """Gets the DeletionTime property"""
        return self.properties.get("DeletionTime", None)

    @property
    def site_id(self) -> Optional[UUID]:
        """Gets the SiteId property"""
        return self.properties.get("SiteId", None)

    @property
    def status(self) -> Optional[str]:
        """Gets the Status property"""
        return self.properties.get("Status", None)

    @property
    def storage_maximum_level(self) -> Optional[int]:
        """Gets the StorageMaximumLevel property"""
        return self.properties.get("StorageMaximumLevel", None)

    @property
    def url(self) -> Optional[str]:
        """Gets the Url property"""
        return self.properties.get("Url", None)

    @property
    def user_code_maximum_level(self) -> Optional[float]:
        """Gets the UserCodeMaximumLevel property"""
        return self.properties.get("UserCodeMaximumLevel", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.DeletedSiteProperties"

from datetime import datetime
from typing import Optional
from uuid import UUID

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class DeletedSiteProperties(Entity):
    @odata(name="ArchiveStatus")
    @property
    def archive_status(self) -> Optional[str]:
        """Gets the ArchiveStatus property"""
        return self.properties.get("ArchiveStatus", None)

    @odata(name="DaysRemaining")
    @property
    def days_remaining(self) -> Optional[int]:
        """Gets the DaysRemaining property"""
        return self.properties.get("DaysRemaining", None)

    @odata(name="DeletionTime")
    @property
    def deletion_time(self) -> Optional[datetime]:
        """Gets the DeletionTime property"""
        return self.properties.get("DeletionTime", None)

    @odata(name="SiteId")
    @property
    def site_id(self) -> Optional[UUID]:
        """Gets the SiteId property"""
        return self.properties.get("SiteId", None)

    @odata(name="Status")
    @property
    def status(self) -> Optional[str]:
        """Gets the Status property"""
        return self.properties.get("Status", None)

    @odata(name="StorageMaximumLevel")
    @property
    def storage_maximum_level(self) -> Optional[int]:
        """Gets the StorageMaximumLevel property"""
        return self.properties.get("StorageMaximumLevel", None)

    @odata(name="Url")
    @property
    def url(self) -> Optional[str]:
        """Gets the Url property"""
        return self.properties.get("Url", None)

    @odata(name="UserCodeMaximumLevel")
    @property
    def user_code_maximum_level(self) -> Optional[float]:
        """Gets the UserCodeMaximumLevel property"""
        return self.properties.get("UserCodeMaximumLevel", None)

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.DeletedSiteProperties"

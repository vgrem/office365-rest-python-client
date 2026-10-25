from __future__ import annotations

from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class StorageQuota(Entity):
    """ """

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.StorageQuota"

    @odata(name="GeoAllocatedStorageMB")
    @property
    def geo_allocated_storage_mb(self) -> Optional[int]:
        """Gets the GeoAllocatedStorageMB property"""
        return self.properties.get("GeoAllocatedStorageMB", None)

    @odata(name="GeoAvailableStorageMB")
    @property
    def geo_available_storage_mb(self) -> Optional[int]:
        """Gets the GeoAvailableStorageMB property"""
        return self.properties.get("GeoAvailableStorageMB", None)

    @odata(name="GeoLocation")
    @property
    def geo_location(self) -> Optional[str]:
        """Gets the GeoLocation property"""
        return self.properties.get("GeoLocation", None)

    @odata(name="GeoUsedArchivedFileStorageMB")
    @property
    def geo_used_archived_file_storage_mb(self) -> Optional[int]:
        """Gets the GeoUsedArchivedFileStorageMB property"""
        return self.properties.get("GeoUsedArchivedFileStorageMB", None)

    @odata(name="GeoUsedArchiveStorageMB")
    @property
    def geo_used_archive_storage_mb(self) -> Optional[int]:
        """Gets the GeoUsedArchiveStorageMB property"""
        return self.properties.get("GeoUsedArchiveStorageMB", None)

    @odata(name="GeoUsedStorageMB")
    @property
    def geo_used_storage_mb(self) -> Optional[int]:
        """Gets the GeoUsedStorageMB property"""
        return self.properties.get("GeoUsedStorageMB", None)

    @odata(name="GeoUsedVersionSizeStorageMB")
    @property
    def geo_used_version_size_storage_mb(self) -> Optional[int]:
        """Gets the GeoUsedVersionSizeStorageMB property"""
        return self.properties.get("GeoUsedVersionSizeStorageMB", None)

    @odata(name="QuotaType")
    @property
    def quota_type(self) -> Optional[int]:
        """Gets the QuotaType property"""
        return self.properties.get("QuotaType", None)

    @odata(name="TenantStorageMB")
    @property
    def tenant_storage_mb(self) -> Optional[int]:
        """Gets the TenantStorageMB property"""
        return self.properties.get("TenantStorageMB", None)

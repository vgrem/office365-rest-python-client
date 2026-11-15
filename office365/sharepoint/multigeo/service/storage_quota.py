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

    @odata(name="GeoUsedArchivedOneDrivePreservationHoldTotalSizeStorageMB")
    @property
    def geo_used_archived_onedrive_preservation_hold_total_size_storage_mb(self) -> Optional[int]:
        """Gets the GeoUsedArchivedOneDrivePreservationHoldTotalSizeStorageMB property"""
        return self.properties.get("GeoUsedArchivedOneDrivePreservationHoldTotalSizeStorageMB", None)

    @odata(name="GeoUsedArchivedOneDrivePreservationHoldVersionSizeStorageMB")
    @property
    def geo_used_archived_onedrive_preservation_hold_version_size_storage_mb(self) -> Optional[int]:
        """Gets the GeoUsedArchivedOneDrivePreservationHoldVersionSizeStorageMB property"""
        return self.properties.get("GeoUsedArchivedOneDrivePreservationHoldVersionSizeStorageMB", None)

    @odata(name="GeoUsedArchivedPreservationHoldTotalSizeStorageMB")
    @property
    def geo_used_archived_preservation_hold_total_size_storage_mb(self) -> Optional[int]:
        """Gets the GeoUsedArchivedPreservationHoldTotalSizeStorageMB property"""
        return self.properties.get("GeoUsedArchivedPreservationHoldTotalSizeStorageMB", None)

    @odata(name="GeoUsedArchivedPreservationHoldVersionSizeStorageMB")
    @property
    def geo_used_archived_preservation_hold_version_size_storage_mb(self) -> Optional[int]:
        """Gets the GeoUsedArchivedPreservationHoldVersionSizeStorageMB property"""
        return self.properties.get("GeoUsedArchivedPreservationHoldVersionSizeStorageMB", None)

    @odata(name="GeoUsedOneDrivePreservationHoldTotalSizeStorageMB")
    @property
    def geo_used_onedrive_preservation_hold_total_size_storage_mb(self) -> Optional[int]:
        """Gets the GeoUsedOneDrivePreservationHoldTotalSizeStorageMB property"""
        return self.properties.get("GeoUsedOneDrivePreservationHoldTotalSizeStorageMB", None)

    @odata(name="GeoUsedOneDrivePreservationHoldVersionSizeStorageMB")
    @property
    def geo_used_onedrive_preservation_hold_version_size_storage_mb(self) -> Optional[int]:
        """Gets the GeoUsedOneDrivePreservationHoldVersionSizeStorageMB property"""
        return self.properties.get("GeoUsedOneDrivePreservationHoldVersionSizeStorageMB", None)

    @odata(name="GeoUsedPreservationHoldTotalSizeStorageMB")
    @property
    def geo_used_preservation_hold_total_size_storage_mb(self) -> Optional[int]:
        """Gets the GeoUsedPreservationHoldTotalSizeStorageMB property"""
        return self.properties.get("GeoUsedPreservationHoldTotalSizeStorageMB", None)

    @odata(name="GeoUsedPreservationHoldVersionSizeStorageMB")
    @property
    def geo_used_preservation_hold_version_size_storage_mb(self) -> Optional[int]:
        """Gets the GeoUsedPreservationHoldVersionSizeStorageMB property"""
        return self.properties.get("GeoUsedPreservationHoldVersionSizeStorageMB", None)

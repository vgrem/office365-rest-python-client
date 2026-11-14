from __future__ import annotations

from datetime import date
from typing import Optional

from office365.entity import Entity
from office365.intune.devices.management.virtualendpoint.cloudpcs.galleryimagestatus import CloudPcGalleryImageStatus
from office365.runtime.types.odata_property import odata


class CloudPcGalleryImage(Entity):
    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="endDate")
    @property
    def end_date(self) -> Optional[date]:
        """Gets the endDate property"""
        return self.properties.get("endDate", None)

    @odata(name="expirationDate")
    @property
    def expiration_date(self) -> Optional[date]:
        """Gets the expirationDate property"""
        return self.properties.get("expirationDate", None)

    @odata(name="offerName")
    @property
    def offer_name(self) -> Optional[str]:
        """Gets the offerName property"""
        return self.properties.get("offerName", None)

    @odata(name="osVersionNumber")
    @property
    def os_version_number(self) -> Optional[str]:
        """Gets the osVersionNumber property"""
        return self.properties.get("osVersionNumber", None)

    @odata(name="publisherName")
    @property
    def publisher_name(self) -> Optional[str]:
        """Gets the publisherName property"""
        return self.properties.get("publisherName", None)

    @odata(name="sizeInGB")
    @property
    def size_in_gb(self) -> Optional[int]:
        """Gets the sizeInGB property"""
        return self.properties.get("sizeInGB", None)

    @odata(name="skuName")
    @property
    def sku_name(self) -> Optional[str]:
        """Gets the skuName property"""
        return self.properties.get("skuName", None)

    @odata(name="startDate")
    @property
    def start_date(self) -> Optional[date]:
        """Gets the startDate property"""
        return self.properties.get("startDate", None)

    @odata(name="status")
    @property
    def status(self) -> CloudPcGalleryImageStatus:
        """Gets the status property"""
        return self.properties.get("status", CloudPcGalleryImageStatus.supported)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CloudPcGalleryImage"

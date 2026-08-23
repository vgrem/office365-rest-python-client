from __future__ import annotations

from dataclasses import field
from datetime import datetime

from office365.runtime.client_value import ClientValue


class CatalogManagementStatus(ClientValue):
    adlsLastUploadFailure: datetime | None = field(default_factory=lambda: datetime.min)
    adlsLastUploadStart: datetime | None = field(default_factory=lambda: datetime.min)
    adlsLastUploadSuccess: datetime | None = field(default_factory=lambda: datetime.min)
    customSitePropertyDataLastUpdated: datetime | None = field(default_factory=lambda: datetime.min)
    displayNamesLastUpdated: datetime | None = field(default_factory=lambda: datetime.min)
    extendedPropertyMapLastUpdated: datetime | None = field(default_factory=lambda: datetime.min)
    schemaLastUpdated: datetime | None = field(default_factory=lambda: datetime.min)
    siteCategoriesCsvLastUploaded: datetime | None = field(default_factory=lambda: datetime.min)
    siteOwnerDataLastUpdated: datetime | None = field(default_factory=lambda: datetime.min)
    uploadToADLSStatus: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Administration.TenantAdmin.CatalogManagement.CatalogManagementStatus"

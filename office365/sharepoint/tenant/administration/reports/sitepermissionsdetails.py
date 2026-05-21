from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SitePermissionsReportDetails(ClientValue):
    anyoneLinksSiteCount: int | None = None
    eeeuPermissionSiteCount: int | None = None
    reportTotalSiteCount: int | None = None
    uniquePermissionSiteCount: int | None = None
    uniqueSiteCount: int | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.SitePermissionsReportDetails"

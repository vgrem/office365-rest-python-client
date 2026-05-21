from __future__ import annotations

from datetime import datetime
from typing import Optional


from dataclasses import dataclass
from office365.runtime.client_value import ClientValue


@dataclass
class UnlicensedOdbTenantMetrics(ClientValue):

    adminLockedCount: Optional[int] = None
    adminLockedSizeBytes: Optional[float] = None
    billableCount: Optional[int] = None
    billableSizeBytes: Optional[float] = None
    complianceHoldCount: Optional[int] = None
    complianceHoldSizeBytes: Optional[float] = None
    count: Optional[int] = None
    duplicateSiteCount: Optional[int] = None
    duplicateSiteSizeBytes: Optional[float] = None
    invalidLicenseCount: Optional[int] = None
    invalidLicenseSizeBytes: Optional[float] = None
    lastRefreshOn: Optional[datetime] = None
    restoredByTenantAdminCount: Optional[int] = None
    restoredByTenantAdminSizeBytes: Optional[float] = None
    retentionPeriodCount: Optional[int] = None
    retentionPeriodSizeBytes: Optional[float] = None
    sizeBytes: Optional[float] = None
    unknownCount: Optional[int] = None
    unknownSizeBytes: Optional[float] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.OdbLicenseEnforcement.UnlicensedOdbTenantMetrics"
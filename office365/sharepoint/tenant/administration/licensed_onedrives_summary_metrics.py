from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class LicensedOneDrivesSummaryMetrics(ClientValue):
    activePayAsYouGoCount: int | None = None
    maxedLicenseQuotaCount: int | None = None
    reachingStorageLimitCount: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Administration.TenantAdmin.OdbMetricsAggregation.LicensedOneDrivesSummaryMetrics"

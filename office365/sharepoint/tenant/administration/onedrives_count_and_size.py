from __future__ import annotations

from office365.runtime.client_value import ClientValue


class OneDrivesCountAndSize(ClientValue):
    count: int | None = None
    sizeBytes: float | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Administration.TenantAdmin.OdbMetricsAggregation.OneDrivesCountAndSize"

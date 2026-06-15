from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class DatasetMetadataRequestInfo(ClientValue):
    feature: str | None = None
    subTypes: StringCollection = field(default_factory=StringCollection)

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Administration.TenantAdmin.SPOAdminReportInsights.Models.DatasetMetadataRequestInfo"

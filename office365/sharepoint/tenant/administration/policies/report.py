from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from office365.runtime.client_value import ClientValue


@dataclass
class TenantAdminPolicyReport(ClientValue):
    policyExecutionTime: datetime | None = None
    policyExecutionId: int | None = None
    policyId: str | None = None
    policyReportDetails: str | None = None
    policyVersion: int | None = None
    reportCreationTime: datetime | None = None
    reportUpdationTime: datetime | None = None
    usersToExclude: str | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.TenantAdminPolicyReport"

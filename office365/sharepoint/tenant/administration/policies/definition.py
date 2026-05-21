from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from office365.runtime.client_value import ClientValue


@dataclass
class TenantAdminPolicyDefinition(ClientValue):
    createdBy: str | None = None
    lastUpdatedTime: datetime | None = None
    policyCreatedTime: datetime | None = None
    policyCustomName: str | None = None
    policyDefinitionDetails: str | None = None
    policyDeleteReason: str | None = None
    policyDescription: str | None = None
    policyFrequencyUnit: int | None = None
    policyFrequencyValue: int | None = None
    policyId: str | None = None
    policyState: int | None = None
    policyTags: str | None = None
    policyTemplate: int | None = None
    policyType: int | None = None
    policyVersion: int | None = None
    updatedBy: str | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.TenantAdminPolicyDefinition"

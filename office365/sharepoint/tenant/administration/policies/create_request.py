from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from office365.runtime.client_value import ClientValue


@dataclass
class CreatePolicyRequest(ClientValue):
    isPreviewRun: bool | None = None
    policyCustomName: str | None = None
    policyDefinitionDetails: str | None = None
    policyDescription: str | None = None
    policyFrequencyUnit: int | None = None
    policyFrequencyValue: int | None = None
    policyId: UUID | None = None
    policyTags: str | None = None
    policyTemplate: int | None = None
    policyType: int | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.CreatePolicyRequest"

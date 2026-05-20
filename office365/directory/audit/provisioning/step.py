from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.audit.provisioning.detailsinfo import DetailsInfo
from office365.directory.audit.provisioning.result import ProvisioningResult
from office365.directory.audit.provisioning.steptype import ProvisioningStepType
from office365.runtime.client_value import ClientValue


@dataclass
class ProvisioningStep(ClientValue):
    description: str | None = None
    details: DetailsInfo = field(default_factory=DetailsInfo)
    name: str | None = None
    provisioningStepType: ProvisioningStepType = ProvisioningStepType.none
    status: ProvisioningResult = ProvisioningResult.none

    @property
    def entity_type_name(self):
        return "microsoft.graph.ProvisioningStep"

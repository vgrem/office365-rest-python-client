from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.audit.provisioning.errorinfo import ProvisioningErrorInfo
from office365.directory.audit.provisioning.result import ProvisioningResult
from office365.runtime.client_value import ClientValue


@dataclass
class ProvisioningStatusInfo(ClientValue):
    errorInformation: ProvisioningErrorInfo = field(default_factory=ProvisioningErrorInfo)
    status: ProvisioningResult | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.ProvisioningStatusInfo"

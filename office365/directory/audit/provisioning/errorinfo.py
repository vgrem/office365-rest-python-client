from __future__ import annotations

from dataclasses import dataclass

from office365.directory.audit.provisioning.statuserrorcategory import ProvisioningStatusErrorCategory
from office365.runtime.client_value import ClientValue


@dataclass
class ProvisioningErrorInfo(ClientValue):
    additionalDetails: str | None = None
    errorCategory: ProvisioningStatusErrorCategory = ProvisioningStatusErrorCategory.none
    errorCode: str | None = None
    reason: str | None = None
    recommendedAction: str | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.ProvisioningErrorInfo"

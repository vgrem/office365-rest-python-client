from __future__ import annotations

from dataclasses import field

from office365.directory.audit.provisioning.detailsinfo import DetailsInfo
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ProvisioningSystem(ClientValue):
    details: DetailsInfo = field(default_factory=DetailsInfo)

    @property
    def entity_type_name(self):
        return "microsoft.graph.ProvisioningSystem"

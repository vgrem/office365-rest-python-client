from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.audit.provisioning.detailsinfo import DetailsInfo
from office365.runtime.client_value import ClientValue


@dataclass
class ProvisionedIdentity(ClientValue):
    details: DetailsInfo = field(default_factory=DetailsInfo)
    identityType: str | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.ProvisionedIdentity"

from __future__ import annotations

from dataclasses import field

from office365.directory.audit.provisioning.detailsinfo import DetailsInfo
from office365.runtime.client_value import ClientValue


class ProvisionedIdentity(ClientValue):
    details: DetailsInfo = field(default_factory=DetailsInfo)
    identityType: str | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.ProvisionedIdentity"

from __future__ import annotations

from dataclasses import dataclass, field

from office365.communications.endpointtype import EndpointType
from office365.directory.permissions.identity import Identity
from office365.runtime.client_value import ClientValue


@dataclass
class CommunicationsIdentitySet(ClientValue):
    applicationInstance: Identity = field(default_factory=Identity)
    assertedIdentity: Identity = field(default_factory=Identity)
    azureCommunicationServicesUser: Identity = field(default_factory=Identity)
    encrypted: Identity = field(default_factory=Identity)
    endpointType: EndpointType = EndpointType.default
    guest: Identity = field(default_factory=Identity)
    onPremises: Identity = field(default_factory=Identity)
    phone: Identity = field(default_factory=Identity)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CommunicationsIdentitySet"

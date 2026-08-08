from __future__ import annotations

from dataclasses import dataclass

from office365.directory.identities.api_connector import IdentityApiConnector
from office365.runtime.client_value import ClientValue


@dataclass
class UserFlowApiConnectorConfiguration(ClientValue):
    postAttributeCollection: IdentityApiConnector | None = None
    postFederationSignup: IdentityApiConnector | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserFlowApiConnectorConfiguration"

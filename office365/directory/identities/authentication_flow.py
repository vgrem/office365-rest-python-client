from __future__ import annotations

from dataclasses import dataclass

from office365.directory.policies.conditionalaccess.transfermethods import ConditionalAccessTransferMethods
from office365.runtime.client_value import ClientValue


@dataclass
class AuthenticationFlow(ClientValue):
    transferMethod: ConditionalAccessTransferMethods = ConditionalAccessTransferMethods.none

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AuthenticationFlow"

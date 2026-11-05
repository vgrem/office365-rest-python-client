from __future__ import annotations

from office365.directory.policies.conditionalaccess.transfermethods import ConditionalAccessTransferMethods
from office365.runtime.client_value import ClientValue


class ConditionalAccessAuthenticationFlows(ClientValue):
    transferMethods: ConditionalAccessTransferMethods = ConditionalAccessTransferMethods.none

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ConditionalAccessAuthenticationFlows"

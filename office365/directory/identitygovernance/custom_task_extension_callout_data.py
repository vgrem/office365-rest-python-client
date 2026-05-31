from __future__ import annotations

from dataclasses import dataclass

from office365.directory.users.user import User
from office365.runtime.client_value import ClientValue


@dataclass
class CustomTaskExtensionCalloutData(ClientValue):
    subject: User | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.identityGovernance.CustomTaskExtensionCalloutData"

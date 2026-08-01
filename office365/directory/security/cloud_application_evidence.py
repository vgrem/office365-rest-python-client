from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class CloudApplicationEvidence(ClientValue):
    appId: int | None = None
    displayName: str | None = None
    instanceId: int | None = None
    instanceName: str | None = None
    saasAppId: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.CloudApplicationEvidence"

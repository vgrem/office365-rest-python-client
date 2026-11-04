from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ProtectionPolicyArtifactCount(ClientValue):
    completed: int | None = None
    failed: int | None = None
    inProgress: int | None = None
    total: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ProtectionPolicyArtifactCount"

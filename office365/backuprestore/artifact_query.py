from __future__ import annotations

from office365.backuprestore.restorableartifact import RestorableArtifact
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ArtifactQuery(ClientValue):
    artifactType: RestorableArtifact = RestorableArtifact.message
    queryExpression: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ArtifactQuery"

from __future__ import annotations

from office365.runtime.client_value import ClientValue


class AccessReviewContextDataBase(ClientValue):
    reviewDefinitionId: str | None = None
    reviewInstanceId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.customDataProvidedResourcePayloads.AccessReviewContextDataBase"

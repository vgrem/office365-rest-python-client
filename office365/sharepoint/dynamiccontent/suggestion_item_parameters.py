from __future__ import annotations

from uuid import UUID

from office365.runtime.client_value import ClientValue


class SuggestionItemParameters(ClientValue):
    Metadata: str | None = None
    PageItemId: int | None = None
    PageItemUniqueId: UUID | None = None
    State: str | None = None
    WebPartInstanceId: UUID | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.DynamicContent.SuggestionItemParameters"

from __future__ import annotations

from office365.runtime.client_value import ClientValue


class FaqSuggestionItem(ClientValue):
    Identifier: str | None = None
    Metadata: str | None = None
    PageItemId: int | None = None
    PageUrl: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.DynamicContent.FaqSuggestionItem"

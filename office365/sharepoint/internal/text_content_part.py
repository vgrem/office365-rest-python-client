from __future__ import annotations

from office365.runtime.client_value import ClientValue


class TextContentPart(ClientValue):
    Text: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Internal.TextContentPart"

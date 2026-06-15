from __future__ import annotations

from office365.runtime.client_value import ClientValue


class ContentControlStdContent(ClientValue):
    ContentControlId: str | None = None
    StdContent: str | None = None
    Tag: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.ContentSolution.Models.Responses.ContentControlStdContent"

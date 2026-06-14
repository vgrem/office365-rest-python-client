from __future__ import annotations

from uuid import UUID

from office365.runtime.client_value import ClientValue


class FAQRequestPayload(ClientValue):
    PageListItemId: int | None = None
    UniqueId: UUID | None = None
    WebPartInstanceId: UUID | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.DynamicContent.FAQRequestPayload"

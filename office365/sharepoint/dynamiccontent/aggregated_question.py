from __future__ import annotations

from office365.runtime.client_value import ClientValue


class AggregatedQuestion(ClientValue):
    AskedCount: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.DynamicContent.AggregatedQuestion"

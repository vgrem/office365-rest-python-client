from __future__ import annotations

from office365.runtime.client_value import ClientValue


class BucketAggregationRange(ClientValue):
    from_: str | None = None
    to: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.BucketAggregationRange"

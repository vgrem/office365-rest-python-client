from __future__ import annotations
from dataclasses import dataclass
from office365.runtime.client_value import ClientValue
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class SubjectRightsRequestDetail(ClientValue):
    excludedItemCount: int | None = None
    insightCounts: ClientValueCollection[KeyValuePair] = field(default_factory=lambda: ClientValueCollection(KeyValuePair))
    itemCount: int | None = None
    itemNeedReview: int | None = None
    productItemCounts: ClientValueCollection[KeyValuePair] = field(default_factory=lambda: ClientValueCollection(KeyValuePair))
    signedOffItemCount: int | None = None
    totalItemSize: int | None = None

    @property
    def entity_type_name(self) -> str:
        return 'microsoft.graph.SubjectRightsRequestDetail'
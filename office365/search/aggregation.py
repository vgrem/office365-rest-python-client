from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.search.bucket import SearchBucket


@dataclass
class SearchAggregation(ClientValue):
    """Provides the details of the search aggregation in the search response."""

    buckets: ClientValueCollection[SearchBucket] = field(default_factory=lambda: ClientValueCollection(SearchBucket))
    field: str | None = None

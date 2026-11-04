from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class SearchBucket(ClientValue):
    """Represents a container for one or more search results that share the same value for the entity field
    that aggregates them.

    Fields:
        aggregationFilterToken (str): A token containing the encoded filter to aggregate search matches by the
           specific key value. To use the filter, pass the token as part of the aggregationFilter property in a
           searchRequest object, in the format "{field}:\"{aggregationFilterToken}\""
        count (int): The approximate number of search matches that share the same value specified in the
           key property. Note that this number is not the exact number of matches.
        key (str): The discrete value of the field that an aggregation was computed on.
    """

    aggregationFilterToken: str | None = None
    count: int | None = None
    key: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SearchBucket"

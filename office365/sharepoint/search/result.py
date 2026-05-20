from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection
from office365.runtime.utilities import parse_key_value_collection
from office365.sharepoint.search.query_result import QueryResult


@dataclass
class SearchResult(ClientValue):
    """
    The SearchResult structure resembles the ResultTableCollection structure
    (specified in [MS-QSSWS] section 3.1.4.1.3.1). However, the individual result tables that share the same
    QueryId are grouped together in a QueryResult structure (specified in section 3.1.5.2).
    The search result tables that have exactly the same QueryId value as specified by the protocol client are grouped
    in the same QueryResult structure accessed through the PrimaryQueryResult property. All other QueryResult buckets
    are organized in a CSOM array of QueryResults accessed through the SecondaryQueryResults property.
    """

    ElapsedTime: str | None = None
    PrimaryQueryResult: QueryResult | None = None
    Properties: dict | None = None
    SecondaryQueryResults: ClientValueCollection[QueryResult] = field(
        default_factory=lambda: ClientValueCollection(QueryResult)
    )
    SpellingSuggestion: str | None = None
    TriggeredRules: StringCollection = field(default_factory=StringCollection)

    def set_property(self, k, v, persist_changes=True):
        if k == "Properties":
            v = parse_key_value_collection(v)
        super().set_property(k, v, persist_changes)
        return self

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.SearchResult"

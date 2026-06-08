from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.search.query.auto_completion_match import (
    QueryAutoCompletionMatch,
)


@dataclass
class QueryAutoCompletion(ClientValue):
    """The QueryAutoCompletion complex type represents the matches for the Query in one Source.

    Args:
        query (str): This element represents the query text for the matched results.
        score (float): This element represents the score for the Query in the Source over all matches in the Source.
        source (str): This element represents the Source used when retrieving the matched results.
    """

    Matches: ClientValueCollection[QueryAutoCompletionMatch] = field(
        default_factory=lambda: ClientValueCollection(QueryAutoCompletionMatch)
    )
    Query: str | None = None
    Score: float | None = None
    Source: str | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Client.Search.Query.QueryAutoCompletion"

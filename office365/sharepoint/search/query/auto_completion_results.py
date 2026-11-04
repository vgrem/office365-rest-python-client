from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value
from office365.sharepoint.search.query.auto_completion import QueryAutoCompletion


@value
class QueryAutoCompletionResults(ClientValue):
    """The complex type QueryAutoCompletionResults represent the result of the operation GetQueryCompletions
    as specified in section 3.1.4.25.2.1."""

    CoreExecutionTimeMs: int | None = None
    CorrelationId: str | None = None
    Queries: ClientValueCollection[QueryAutoCompletion] = field(
        default_factory=lambda: ClientValueCollection(QueryAutoCompletion)
    )

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Client.Search.Query.QueryAutoCompletionResults"

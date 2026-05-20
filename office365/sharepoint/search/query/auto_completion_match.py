from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class QueryAutoCompletionMatch(ClientValue):
    """Represents one match in the Source for the Query"""

    Alternation: str | None = None
    Key: str | None = None
    Length: int | None = None
    MatchType: str | None = None
    Score: float | None = None
    SourceName: str | None = None
    Start: int | None = None
    Value: str | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Client.Search.Query.QueryAutoCompletionMatch"

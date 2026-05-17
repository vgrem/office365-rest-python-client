from typing import Optional

from office365.runtime.client_value import ClientValue


class QueryAutoCompletionMatch(ClientValue):
    """Represents one match in the Source for the Query"""

    def __init__(
        self,
        alternation=None,
        key=None,
        length: Optional[int] = None,
        match_type: Optional[str] = None,
        score: Optional[float] = None,
        source_name: Optional[str] = None,
        start: Optional[int] = None,
        value: Optional[str] = None,
    ):
        """ """
        self.Alternation = alternation
        self.Key = key
        self.Length = length
        self.MatchType = match_type
        self.Score = score
        self.SourceName = source_name
        self.Start = start
        self.Value = value

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Client.Search.Query.QueryAutoCompletionMatch"

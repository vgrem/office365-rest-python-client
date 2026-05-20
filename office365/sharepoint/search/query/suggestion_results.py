from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.search.query.personal_result_suggestion import (
    PersonalResultSuggestion,
)
from office365.sharepoint.search.query.suggestionquery import QuerySuggestionQuery


@dataclass
class QuerySuggestionResults(ClientValue):
    """
    The QuerySuggestionResults complex type is a container for arrays of query suggestions, people name suggestions,
    and personal result suggestions.
    """

    PeopleNames: StringCollection = field(default_factory=StringCollection)
    PersonalResults: ClientValueCollection[PersonalResultSuggestion] = field(
        default_factory=lambda: ClientValueCollection(PersonalResultSuggestion)
    )
    PopularResults: ClientValueCollection[PersonalResultSuggestion] = field(
        default_factory=lambda: ClientValueCollection(PersonalResultSuggestion)
    )
    Queries: ClientValueCollection[QuerySuggestionQuery] = field(
        default_factory=lambda: ClientValueCollection(QuerySuggestionQuery)
    )

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Client.Search.Query.QuerySuggestionResults"

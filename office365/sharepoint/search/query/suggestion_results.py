from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.search.query.personal_result_suggestion import (
    PersonalResultSuggestion,
)
from office365.sharepoint.search.query.suggestionquery import QuerySuggestionQuery


class QuerySuggestionResults(ClientValue):
    """
    The QuerySuggestionResults complex type is a container for arrays of query suggestions, people name suggestions,
    and personal result suggestions.
    """

    def __init__(
        self,
        people_names: StringCollection = StringCollection(),
        personal_results=ClientValueCollection(PersonalResultSuggestion),
        popular_results=ClientValueCollection(PersonalResultSuggestion),
        queries=ClientValueCollection(QuerySuggestionQuery),
    ):
        """
        :param list[str] people_names: People names suggested for the user query. MUST be null if
            ShowPeopleNameSuggestions in properties input element is set to false.
        """
        self.PeopleNames = people_names
        self.PersonalResults = personal_results
        self.PopularResults = popular_results
        self.Queries = queries

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Client.Search.Query.QuerySuggestionResults"

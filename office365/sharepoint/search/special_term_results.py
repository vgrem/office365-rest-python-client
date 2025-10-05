from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.search.special_term_result import SpecialTermResult


class SpecialTermResults(ClientValue):
    """The SpecialTermResults table contains best bets that apply to the search query."""

    def __init__(
        self,
        results=None,
        group_template_id: str = None,
        item_template_id: str = None,
        properties: dict = None,
        result_title: str = None,
        result_title_url: str = None,
    ):
        self.Results = ClientValueCollection(SpecialTermResult, results)
        self.GroupTemplateId = group_template_id
        self.ItemTemplateId = item_template_id
        self.Properties = properties
        self.ResultTitle = result_title
        self.ResultTitleUrl = result_title_url

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.SpecialTermResults"

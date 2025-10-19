from datetime import datetime

from office365.runtime.client_value import ClientValue


class SuggestionItem(ClientValue):

    def __init__(
        self,
        dismissed_date: datetime = None,
        identifier: str = None,
        state: int = None,
        suggestion_type: int = None,
        metadata: str = None,
    ):
        self.DismissedDate = dismissed_date
        self.Identifier = identifier
        self.State = state
        self.SuggestionType = suggestion_type
        self.Metadata = metadata

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.SiteManager.SuggestionItem"

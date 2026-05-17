from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


class SuggestionItem(ClientValue):
    def __init__(
        self,
        dismissed_date: Optional[datetime] = None,
        identifier: Optional[str] = None,
        state: Optional[int] = None,
        suggestion_type: Optional[int] = None,
        metadata: Optional[str] = None,
    ):
        self.DismissedDate = dismissed_date
        self.Identifier = identifier
        self.State = state
        self.SuggestionType = suggestion_type
        self.Metadata = metadata

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.SiteManager.SuggestionItem"

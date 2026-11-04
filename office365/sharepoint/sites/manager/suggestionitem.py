from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class SuggestionItem(ClientValue):
    DismissedDate: Optional[datetime] = None
    Identifier: Optional[str] = None
    State: Optional[int] = None
    SuggestionType: Optional[int] = None
    Metadata: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.SiteManager.SuggestionItem"

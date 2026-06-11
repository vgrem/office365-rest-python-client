from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sites.site_suggestion_item import SiteSuggestionItem


class SiteSuggestionResponse(ClientValue):
    items: ClientValueCollection[SiteSuggestionItem] = field(
        default_factory=lambda: ClientValueCollection(SiteSuggestionItem)
    )

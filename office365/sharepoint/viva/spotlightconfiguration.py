from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.viva.newssite import NewsSite
from office365.sharepoint.viva.spotlightnews import SpotlightNews


@dataclass
class SpotlightConfiguration(ClientValue):
    IsHidden: Optional[bool] = None
    NewsSource: Optional[int] = None
    PinnedNews: ClientValueCollection[SpotlightNews] = field(
        default_factory=lambda: ClientValueCollection(SpotlightNews)
    )
    SelectedSites: ClientValueCollection[NewsSite] = field(default_factory=lambda: ClientValueCollection(NewsSite))

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.EmployeeEngagement.SpotlightConfiguration"

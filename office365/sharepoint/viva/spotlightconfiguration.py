from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.viva.newssite import NewsSite
from office365.sharepoint.viva.spotlightnews import SpotlightNews


class SpotlightConfiguration(ClientValue):

    def __init__(
        self,
        is_hidden: bool = None,
        news_source: int = None,
        pinned_news: ClientValueCollection[SpotlightNews] = ClientValueCollection(
            SpotlightNews
        ),
        selected_sites: ClientValueCollection[NewsSite] = ClientValueCollection(
            NewsSite
        ),
    ):
        self.IsHidden = is_hidden
        self.NewsSource = news_source
        self.PinnedNews = pinned_news
        self.SelectedSites = selected_sites

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.EmployeeEngagement.SpotlightConfiguration"

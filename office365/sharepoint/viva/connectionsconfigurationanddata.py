from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.viva.home_title_region import VivaHomeTitleRegion
from office365.sharepoint.viva.spotlightconfiguration import SpotlightConfiguration
from office365.sharepoint.viva.spotlightnews import SpotlightNews


class ConnectionsConfigurationAndData(ClientValue):

    def __init__(
        self,
        is_configured: bool = None,
        spotlight_configuration: SpotlightConfiguration = SpotlightConfiguration(),
        spotlight_news: ClientValueCollection[SpotlightNews] = ClientValueCollection(
            SpotlightNews
        ),
        title_region: VivaHomeTitleRegion = VivaHomeTitleRegion(),
    ):
        self.IsConfigured = is_configured
        self.SpotlightConfiguration = spotlight_configuration
        self.SpotlightNews = spotlight_news
        self.TitleRegion = title_region

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.EmployeeEngagement.ConnectionsConfigurationAndData"

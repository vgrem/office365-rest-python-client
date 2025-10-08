from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.viva.home_title_region import VivaHomeTitleRegion
from office365.sharepoint.viva.resource_link import VivaResourceLink
from office365.sharepoint.viva.spotlightconfiguration import SpotlightConfiguration


class VCConfiguration(ClientValue):

    def __init__(
        self,
        company_links: ClientValueCollection[VivaResourceLink] = ClientValueCollection(
            VivaResourceLink
        ),
        spotlight_configuration: SpotlightConfiguration = SpotlightConfiguration(),
        title_region: VivaHomeTitleRegion = VivaHomeTitleRegion(),
    ):
        self.CompanyLinks = company_links
        self.SpotlightConfiguration = spotlight_configuration
        self.TitleRegion = title_region

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.EmployeeEngagement.VCConfiguration"

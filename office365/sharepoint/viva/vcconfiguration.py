from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.viva.home_title_region import VivaHomeTitleRegion
from office365.sharepoint.viva.resource_link import VivaResourceLink
from office365.sharepoint.viva.spotlightconfiguration import SpotlightConfiguration


@dataclass
class VCConfiguration(ClientValue):
    CompanyLinks: ClientValueCollection[VivaResourceLink] = field(
        default_factory=lambda: ClientValueCollection(VivaResourceLink)
    )
    SpotlightConfiguration: SpotlightConfiguration = field(default_factory=SpotlightConfiguration)
    TitleRegion: VivaHomeTitleRegion = field(default_factory=VivaHomeTitleRegion)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.EmployeeEngagement.VCConfiguration"

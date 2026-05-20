from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.viva.home_title_region import VivaHomeTitleRegion
from office365.sharepoint.viva.spotlightconfiguration import SpotlightConfiguration
from office365.sharepoint.viva.spotlightnews import SpotlightNews


@dataclass
class ConnectionsConfigurationAndData(ClientValue):
    IsConfigured: Optional[bool] = None
    SpotlightConfiguration: SpotlightConfiguration = field(default_factory=SpotlightConfiguration)
    SpotlightNews: ClientValueCollection[SpotlightNews] = field(
        default_factory=lambda: ClientValueCollection(SpotlightNews)
    )
    TitleRegion: VivaHomeTitleRegion = field(default_factory=VivaHomeTitleRegion)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.EmployeeEngagement.ConnectionsConfigurationAndData"

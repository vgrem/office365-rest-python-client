from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.paths.resource_path import ResourcePath
from office365.sharepoint.sitedesigns.mobile_settings import MobileSettings
from office365.sharepoint.sites.home.navconfiguration import HomeSiteNavConfiguration


@dataclass
class ConfigurationData(ClientValue):
    AppSettings: MobileSettings = field(default_factory=MobileSettings)
    BridgeAbsolutePath: ResourcePath = field(default_factory=ResourcePath)
    HomeSiteTitle: str | None = None
    IsCustomizedThemeEnabled: bool | None = None
    IsPersonalizationEnabled: bool | None = None
    IsVivaHomeFeedReplaceFlightEnabled: bool | None = None
    IsVivaHomeOptedOut: bool | None = None
    NavConfig: HomeSiteNavConfiguration = field(default_factory=HomeSiteNavConfiguration)
    SiteId: UUID | None = None
    Theme: str | None = None
    VivaExperienceType: int | None = None
    WebId: UUID | None = None

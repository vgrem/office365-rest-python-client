from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.paths.resource_path import ResourcePath
from office365.sharepoint.sites.home.navconfiguration import HomeSiteNavConfiguration


@dataclass
class ConfigurationData(ClientValue):
    bridge_absolute_path: Optional[ResourcePath] = None
    is_customized_theme_enabled: Optional[bool] = None
    is_personalization_enabled: Optional[bool] = None
    is_viva_home_feed_replace_flight_enabled: Optional[bool] = None
    is_viva_home_opted_out: Optional[bool] = None
    nav_config: Optional[HomeSiteNavConfiguration] = None
    site_id: Optional[str] = None
    theme: Optional[str] = None
    viva_experience_type: Optional[int] = None
    web_id: Optional[str] = None

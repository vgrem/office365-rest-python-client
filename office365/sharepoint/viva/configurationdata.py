from office365.runtime.client_value import ClientValue
from office365.runtime.paths.resource_path import ResourcePath
from office365.sharepoint.sites.home.navconfiguration import HomeSiteNavConfiguration
from typing import Optional


class ConfigurationData(ClientValue):
    def __init__(
        self,
        bridge_absolute_path: Optional[ResourcePath] = None,
        is_customized_theme_enabled: Optional[bool] = None,
        is_personalization_enabled: Optional[bool] = None,
        is_viva_home_feed_replace_flight_enabled: Optional[bool] = None,
        is_viva_home_opted_out: Optional[bool] = None,
        nav_config: Optional[HomeSiteNavConfiguration] = None,
        site_id: Optional[str] = None,
        theme: Optional[str] = None,
        viva_experience_type: Optional[int] = None,
        web_id: Optional[str] = None,
    ):
        self.bridge_absolute_path = bridge_absolute_path
        self.is_customized_theme_enabled = is_customized_theme_enabled
        self.is_personalization_enabled = is_personalization_enabled
        self.is_viva_home_feed_replace_flight_enabled = is_viva_home_feed_replace_flight_enabled
        self.is_viva_home_opted_out = is_viva_home_opted_out
        self.nav_config = nav_config
        self.site_id = site_id
        self.theme = theme
        self.viva_experience_type = viva_experience_type
        self.web_id = web_id

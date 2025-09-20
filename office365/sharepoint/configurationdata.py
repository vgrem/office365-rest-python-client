from office365.runtime.client_value import ClientValue
from office365.runtime.paths.resource_path import ResourcePath
from office365.sharepoint.homesite.navconfiguration import HomeSiteNavConfiguration


class ConfigurationData(ClientValue):

    def __init__(
        self,
        bridge_absolute_path: ResourcePath = None,
        is_customized_theme_enabled: bool = None,
        is_personalization_enabled: bool = None,
        is_viva_home_feed_replace_flight_enabled: bool = None,
        is_viva_home_opted_out: bool = None,
        nav_config: HomeSiteNavConfiguration = None,
        site_id: str = None,
        theme: str = None,
        viva_experience_type: int = None,
        web_id: str = None,
    ):
        self.bridge_absolute_path = bridge_absolute_path
        self.is_customized_theme_enabled = is_customized_theme_enabled
        self.is_personalization_enabled = is_personalization_enabled
        self.is_viva_home_feed_replace_flight_enabled = (
            is_viva_home_feed_replace_flight_enabled
        )
        self.is_viva_home_opted_out = is_viva_home_opted_out
        self.nav_config = nav_config
        self.site_id = site_id
        self.theme = theme
        self.viva_experience_type = viva_experience_type
        self.web_id = web_id

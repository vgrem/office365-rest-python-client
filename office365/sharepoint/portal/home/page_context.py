from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class SharePointHomePageContext(ClientValue):
    def __init__(
        self,
        active_flights: Optional[StringCollection] = None,
        alternate_web_app_host: Optional[str] = None,
        experience_state: Optional[int] = None,
        is_graph_enabled: Optional[bool] = None,
        is_group_creation_new_ux_enabled: Optional[bool] = None,
        is_logging_upload_enabled: Optional[bool] = None,
        is_mobile: Optional[bool] = None,
        is_modern_search_enabled: Optional[bool] = None,
        is_org_links_provisioned: Optional[bool] = None,
        is_rtl: Optional[bool] = None,
        is_self_service_site_creation_enabled: Optional[bool] = None,
        is_user_voice_enabled: Optional[bool] = None,
        load_suite_nav: Optional[bool] = None,
        microservice_flights: StringCollection = StringCollection(),
        microservice_url: Optional[str] = None,
        my_site_url: Optional[str] = None,
        search_center_url: Optional[str] = None,
        show_create_news_teaching_bubble: Optional[bool] = None,
        show_first_run_experience: Optional[bool] = None,
        show_mobile_upsell: Optional[bool] = None,
        user_acronym: Optional[str] = None,
        user_banner_color: Optional[str] = None,
        user_photo_cdn_base_url: Optional[str] = None,
        video_channel_url_template: Optional[str] = None,
        video_player_url_template: Optional[str] = None,
    ):
        self.ActiveFlights = active_flights
        self.AlternateWebAppHost = alternate_web_app_host
        self.ExperienceState = experience_state
        self.IsGraphEnabled = is_graph_enabled
        self.IsGroupCreationNewUXEnabled = is_group_creation_new_ux_enabled
        self.IsLoggingUploadEnabled = is_logging_upload_enabled
        self.IsMobile = is_mobile
        self.IsModernSearchEnabled = is_modern_search_enabled
        self.IsOrgLinksProvisioned = is_org_links_provisioned
        self.IsRtl = is_rtl
        self.IsSelfServiceSiteCreationEnabled = is_self_service_site_creation_enabled
        self.IsUserVoiceEnabled = is_user_voice_enabled
        self.LoadSuiteNav = load_suite_nav
        self.MicroserviceFlights = microservice_flights
        self.MicroserviceUrl = microservice_url
        self.MySiteUrl = my_site_url
        self.SearchCenterUrl = search_center_url
        self.ShowCreateNewsTeachingBubble = show_create_news_teaching_bubble
        self.ShowFirstRunExperience = show_first_run_experience
        self.ShowMobileUpsell = show_mobile_upsell
        self.UserAcronym = user_acronym
        self.UserBannerColor = user_banner_color
        self.UserPhotoCdnBaseUrl = user_photo_cdn_base_url
        self.VideoChannelUrlTemplate = video_channel_url_template
        self.VideoPlayerUrlTemplate = video_player_url_template

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.Home.SharePointHomePageContext"

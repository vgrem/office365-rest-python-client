from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class SharePointHomePageContext(ClientValue):
    def __init__(
        self,
        active_flights: StringCollection = None,
        alternate_web_app_host: str = None,
        experience_state: int = None,
        is_graph_enabled: bool = None,
        is_group_creation_new_ux_enabled: bool = None,
        is_logging_upload_enabled: bool = None,
        is_mobile: bool = None,
        is_modern_search_enabled: bool = None,
        is_org_links_provisioned: bool = None,
        is_rtl: bool = None,
        is_self_service_site_creation_enabled: bool = None,
        is_user_voice_enabled: bool = None,
        load_suite_nav: bool = None,
        microservice_flights: StringCollection = StringCollection(),
        microservice_url: str = None,
        my_site_url: str = None,
        search_center_url: str = None,
        show_create_news_teaching_bubble: bool = None,
        show_first_run_experience: bool = None,
        show_mobile_upsell: bool = None,
        user_acronym: str = None,
        user_banner_color: str = None,
        user_photo_cdn_base_url: str = None,
        video_channel_url_template: str = None,
        video_player_url_template: str = None,
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

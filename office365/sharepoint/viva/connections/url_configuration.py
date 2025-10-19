from office365.runtime.client_value import ClientValue


class VivaConnectionsUrlConfiguration(ClientValue):

    def __init__(
        self,
        content_url=None,
        dashboard_not_configured_warning=None,
        global_nav_not_configured_warning: str = None,
        not_home_site_url_warning: str = None,
        search_url: str = None,
    ):
        """
        :param str content_url:
        :param str dashboard_not_configured_warning:
        """
        self.ContentUrl = content_url
        self.DashboardNotConfiguredWarning = dashboard_not_configured_warning
        self.GlobalNavNotConfiguredWarning = global_nav_not_configured_warning
        self.NotHomeSiteUrlWarning = not_home_site_url_warning
        self.SearchUrl = search_url

from typing import Optional

from office365.runtime.client_value import ClientValue


class VivaConnectionsUrlConfiguration(ClientValue):
    def __init__(
        self,
        content_url=None,
        dashboard_not_configured_warning=None,
        global_nav_not_configured_warning: Optional[str] = None,
        not_home_site_url_warning: Optional[str] = None,
        search_url: Optional[str] = None,
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

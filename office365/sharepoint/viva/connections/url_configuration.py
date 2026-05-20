from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class VivaConnectionsUrlConfiguration(ClientValue):
    """Viva Connections URL configuration.

    Fields:
        content_url (str):
        dashboard_not_configured_warning (str):
    """

    ContentUrl: Optional[str] = None
    DashboardNotConfiguredWarning: Optional[str] = None
    GlobalNavNotConfiguredWarning: Optional[str] = None
    NotHomeSiteUrlWarning: Optional[str] = None
    SearchUrl: Optional[str] = None

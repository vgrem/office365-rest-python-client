from typing import Optional

from office365.runtime.client_value import ClientValue


class AppProperties(ClientValue):
    def __init__(
        self,
        app_settings_enabled: Optional[bool] = None,
        description: Optional[str] = None,
        eula_url: Optional[str] = None,
        is_anonymous: Optional[bool] = None,
        is_disabled: Optional[bool] = None,
        managed_deployment_enabled: Optional[bool] = None,
        manage_permissions_enabled: Optional[bool] = None,
        manage_seats_enabled: Optional[bool] = None,
        monitoring_enabled: Optional[bool] = None,
        publisher: Optional[str] = None,
        remove_enabled: Optional[bool] = None,
        side_load_enabled: Optional[bool] = None,
        support_url: Optional[str] = None,
        view_in_market_place_enabled: Optional[bool] = None,
    ):
        self.AppSettingsEnabled = app_settings_enabled
        self.Description = description
        self.EulaUrl = eula_url
        self.IsAnonymous = is_anonymous
        self.IsDisabled = is_disabled
        self.ManagedDeploymentEnabled = managed_deployment_enabled
        self.ManagePermissionsEnabled = manage_permissions_enabled
        self.ManageSeatsEnabled = manage_seats_enabled
        self.MonitoringEnabled = monitoring_enabled
        self.Publisher = publisher
        self.RemoveEnabled = remove_enabled
        self.SideLoadEnabled = side_load_enabled
        self.SupportUrl = support_url
        self.ViewInMarketPlaceEnabled = view_in_market_place_enabled

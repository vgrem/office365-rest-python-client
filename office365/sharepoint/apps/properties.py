from office365.runtime.client_value import ClientValue


class AppProperties(ClientValue):

    def __init__(
        self,
        app_settings_enabled: bool = None,
        description: str = None,
        eula_url: str = None,
        is_anonymous: bool = None,
        is_disabled: bool = None,
        managed_deployment_enabled: bool = None,
        manage_permissions_enabled: bool = None,
        manage_seats_enabled: bool = None,
        monitoring_enabled: bool = None,
        publisher: str = None,
        remove_enabled: bool = None,
        side_load_enabled: bool = None,
        support_url: str = None,
        view_in_market_place_enabled: bool = None,
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

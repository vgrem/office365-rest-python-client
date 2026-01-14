from office365.runtime.client_value import ClientValue


class SettingDataProperty(ClientValue):
    def __init__(
        self,
        available_in_graph: bool = None,
        available_in_power_shell: bool = None,
        available_in_share_point_admin_center: bool = None,
        category: int = None,
        description: str = None,
        setting_name: str = None,
        setting_value: str = None,
    ):
        self.AvailableInGraph = available_in_graph
        self.AvailableInPowerShell = available_in_power_shell
        self.AvailableInSharePointAdminCenter = available_in_share_point_admin_center
        self.Category = category
        self.Description = description
        self.SettingName = setting_name
        self.SettingValue = setting_value

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SettingDataProperty"

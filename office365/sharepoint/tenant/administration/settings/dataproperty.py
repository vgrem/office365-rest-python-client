from office365.runtime.client_value import ClientValue
from typing import Optional


class SettingDataProperty(ClientValue):
    def __init__(
        self,
        available_in_graph: Optional[bool] = None,
        available_in_power_shell: Optional[bool] = None,
        available_in_share_point_admin_center: Optional[bool] = None,
        category: Optional[int] = None,
        description: Optional[str] = None,
        setting_name: Optional[str] = None,
        setting_value: Optional[str] = None,
    ):
        self.AvailableInGraph = available_in_graph
        self.AvailableInPowerShell = available_in_power_shell
        self.AvailableInSharePointAdminCenter = available_in_share_point_admin_center
        self.Category = category
        self.Description = description
        self.SettingName = setting_name
        self.SettingValue = setting_value

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SettingDataProperty"

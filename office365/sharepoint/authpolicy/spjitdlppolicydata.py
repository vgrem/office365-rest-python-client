from office365.runtime.client_value import ClientValue


class SPJitDlpPolicyData(ClientValue):

    def __init__(
        self,
        execution_mode: int = None,
        is_policy_enabled: bool = None,
        odb_sensitivity_refresh_window_in_hours: int = None,
    ):
        self.ExecutionMode = execution_mode
        self.IsPolicyEnabled = is_policy_enabled
        self.ODBSensitivityRefreshWindowInHours = odb_sensitivity_refresh_window_in_hours

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.AuthPolicy.SPJitDlpPolicyData"

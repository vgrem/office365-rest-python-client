from office365.runtime.client_value import ClientValue


class SPOServicePrioritizationAppRegistration(ClientValue):
    def __init__(
        self,
        app_id: str = None,
        enabled: bool = None,
        policy_id: str = None,
        quota_multiplier: int = None,
    ):
        self.AppId = app_id
        self.Enabled = enabled
        self.PolicyId = policy_id
        self.QuotaMultiplier = quota_multiplier

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOServicePrioritizationAppRegistration"

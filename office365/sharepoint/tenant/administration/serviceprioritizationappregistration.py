from office365.runtime.client_value import ClientValue
from typing import Optional


class SPOServicePrioritizationAppRegistration(ClientValue):
    def __init__(
        self,
        app_id: Optional[str] = None,
        enabled: Optional[bool] = None,
        policy_id: Optional[str] = None,
        quota_multiplier: Optional[int] = None,
    ):
        self.AppId = app_id
        self.Enabled = enabled
        self.PolicyId = policy_id
        self.QuotaMultiplier = quota_multiplier

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOServicePrioritizationAppRegistration"

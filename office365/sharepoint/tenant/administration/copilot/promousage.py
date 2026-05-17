from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.tenant.administration.monthlyusage import MonthlyUsage
from typing import Optional


class SPOCopilotPromoUsage(ClientValue):
    def __init__(
        self,
        is_copilot_promo_eligible: Optional[bool] = None,
        is_copilot_promo_status_enabled: Optional[bool] = None,
        monthly_usage: ClientValueCollection[MonthlyUsage] = ClientValueCollection(MonthlyUsage),
    ):
        self.IsCopilotPromoEligible = is_copilot_promo_eligible
        self.IsCopilotPromoStatusEnabled = is_copilot_promo_status_enabled
        self.MonthlyUsage = monthly_usage

    ""

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOCopilotPromoUsage"

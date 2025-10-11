from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.tenant.administration.monthlyusage import MonthlyUsage


class SPOCopilotPromoUsage(ClientValue):

    def __init__(
        self,
        is_copilot_promo_eligible: bool = None,
        is_copilot_promo_status_enabled: bool = None,
        monthly_usage: ClientValueCollection[MonthlyUsage] = ClientValueCollection(
            MonthlyUsage
        ),
    ):
        self.IsCopilotPromoEligible = is_copilot_promo_eligible
        self.IsCopilotPromoStatusEnabled = is_copilot_promo_status_enabled
        self.MonthlyUsage = monthly_usage

    ""

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOCopilotPromoUsage"

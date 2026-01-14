from office365.runtime.client_value import ClientValue


class MonthlyUsage(ClientValue):
    def __init__(
        self,
        created_date: str = None,
        promotion_granted: int = None,
        promotion_remaining: int = None,
        promotion_used: int = None,
    ):
        self.CreatedDate = created_date
        self.PromotionGranted = promotion_granted
        self.PromotionRemaining = promotion_remaining
        self.PromotionUsed = promotion_used

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.MonthlyUsage"

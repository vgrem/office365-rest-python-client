from typing import Optional

from office365.runtime.client_value import ClientValue


class MonthlyUsage(ClientValue):
    def __init__(
        self,
        created_date: Optional[str] = None,
        promotion_granted: Optional[int] = None,
        promotion_remaining: Optional[int] = None,
        promotion_used: Optional[int] = None,
    ):
        self.CreatedDate = created_date
        self.PromotionGranted = promotion_granted
        self.PromotionRemaining = promotion_remaining
        self.PromotionUsed = promotion_used

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.MonthlyUsage"

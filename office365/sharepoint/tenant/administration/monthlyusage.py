from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class MonthlyUsage(ClientValue):
    CreatedDate: str | None = None
    PromotionGranted: int | None = None
    PromotionRemaining: int | None = None
    PromotionUsed: int | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.MonthlyUsage"

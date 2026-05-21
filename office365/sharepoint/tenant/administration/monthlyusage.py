from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class MonthlyUsage(ClientValue):
    CreatedDate: str | None = None
    PromotionGranted: int | None = None
    PromotionRemaining: int | None = None
    PromotionUsed: int | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.MonthlyUsage"

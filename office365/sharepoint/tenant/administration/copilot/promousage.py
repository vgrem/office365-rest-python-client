from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.tenant.administration.monthlyusage import MonthlyUsage


@dataclass
class SPOCopilotPromoUsage(ClientValue):
    IsCopilotPromoEligible: bool | None = None
    IsCopilotPromoStatusEnabled: bool | None = None
    MonthlyUsage: ClientValueCollection[MonthlyUsage] = field(
        default_factory=lambda: ClientValueCollection(MonthlyUsage)
    )

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOCopilotPromoUsage"

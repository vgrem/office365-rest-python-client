from office365.runtime.client_value import ClientValue
from typing import Optional


class PowerAppsEnvironment(ClientValue):
    """ """

    def __init__(
        self,
        allocated_ai_credits: Optional[float] = None,
        display_name: Optional[str] = None,
        is_default: Optional[bool] = None,
        name: Optional[str] = None,
        purchased_ai_credits: Optional[float] = None,
    ) -> None:
        self.AllocatedAICredits = allocated_ai_credits
        self.DisplayName = display_name
        self.IsDefault = is_default
        self.Name = name
        self.PurchasedAICredits = purchased_ai_credits

    def __str__(self):
        return self.DisplayName or self.entity_type_name

    def __repr__(self):
        return self.Name or self.entity_type_name

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.TenantAdministration.PowerAppsEnvironment"

from office365.runtime.client_value import ClientValue


class PowerAppsEnvironment(ClientValue):
    """ """

    def __init__(
        self,
        allocated_ai_credits: float = None,
        display_name: str = None,
        is_default: bool = None,
        name: str = None,
        purchased_ai_credits: float = None,
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

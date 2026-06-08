from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class HubSitePermission(ClientValue):
    """Args:
        display_name (str):
        principal_name (str):
        rights (int):
    """

    DisplayName = None
    PrincipalName = None
    Rights = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.HubSitePermission"

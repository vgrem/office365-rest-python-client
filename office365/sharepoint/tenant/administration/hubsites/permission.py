from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class HubSitePermission(ClientValue):
    """:param str display_name:
    :param str principal_name:
    :param int rights:"""

    DisplayName = None
    PrincipalName = None
    Rights = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.HubSitePermission"

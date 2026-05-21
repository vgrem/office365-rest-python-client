from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class PowerAppsEnvironmentContext(ClientValue):
    DataverseInstanceUrl = None
    DisplayName = None
    IsTestEnvironment = None
    LastGetEnvironmentError = None
    Name = None
    UpdatedUTC = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.TenantAdministration.PowerAppsEnvironmentContext"

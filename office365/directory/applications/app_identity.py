from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class AppIdentity(ClientValue):
    """Indicates the identity of the application that performed the action or was changed.
    Includes application ID, name, and service principal ID and name. This resource is used by the
    Get directoryAudit operation.

    Args:
        appId (str): Refers to the Unique GUID representing Application Id in the Azure Active Directory.
        displayName (str): Refers to the Application Name displayed in the Azure Portal.
        servicePrincipalId (str): Refers to the Unique GUID indicating Service Principal Id in Azure Active Directory
          for the corresponding App.
        servicePrincipalName (str): Refers to the Service Principal Name is the Application name in the tenant.
    """

    appId: str | None = None
    displayName: str | None = None
    servicePrincipalId: str | None = None
    servicePrincipalName: str | None = None

    def __str__(self) -> str:
        return self.displayName or self.servicePrincipalName or ""

    def __repr__(self) -> str:
        return self.appId or self.servicePrincipalId or ""

    @property
    def entity_type_name(self):
        return "microsoft.graph.AppIdentity"

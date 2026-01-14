from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.tenant.administration.serviceprioritizationappregistration import (
    SPOServicePrioritizationAppRegistration,
)


class SPOServicePrioritizationAppRegistrations(ClientValue):
    def __init__(
        self,
        registrations: ClientValueCollection[SPOServicePrioritizationAppRegistration] = ClientValueCollection(
            SPOServicePrioritizationAppRegistration
        ),
    ):
        self.Registrations = registrations

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOServicePrioritizationAppRegistrations"

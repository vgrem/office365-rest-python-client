from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.tenant.administration.serviceprioritizationappregistration import (
    SPOServicePrioritizationAppRegistration,
)


@dataclass
class SPOServicePrioritizationAppRegistrations(ClientValue):
    Registrations: ClientValueCollection[SPOServicePrioritizationAppRegistration] = field(
        default_factory=lambda: ClientValueCollection(SPOServicePrioritizationAppRegistration)
    )

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOServicePrioritizationAppRegistrations"

from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.portal.linkedsites.contract import LinkedSiteContract


@dataclass
class LinkedSitesListContract(ClientValue):
    LinkedSites: ClientValueCollection[LinkedSiteContract] = field(
        default_factory=lambda: ClientValueCollection(LinkedSiteContract)
    )

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.LinkedSitesListContract"

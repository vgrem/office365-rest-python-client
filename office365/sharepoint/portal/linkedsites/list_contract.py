from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value
from office365.sharepoint.portal.linkedsites.contract import LinkedSiteContract


@value
class LinkedSitesListContract(ClientValue):
    LinkedSites: ClientValueCollection[LinkedSiteContract] = field(
        default_factory=lambda: ClientValueCollection(LinkedSiteContract)
    )

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.LinkedSitesListContract"

from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sites.manager.missinglink import MissingLink


@dataclass
class MissingLinksResult(ClientValue):
    MissingLinks: ClientValueCollection[MissingLink] = field(default_factory=lambda: ClientValueCollection(MissingLink))

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.SiteManager.MissingLinksResult"

from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sites.manager.retirablepagemetadata import (
    RetirablePageMetadata,
)


@dataclass
class RetirablePagesQueryResult(ClientValue):
    Files: ClientValueCollection[RetirablePageMetadata] = field(
        default_factory=lambda: ClientValueCollection(RetirablePageMetadata)
    )

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.SiteManager.RetirablePagesQueryResult"

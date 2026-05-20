from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sites.manager.missinglinkreferrer import MissingLinkReferrer


@dataclass
class MissingLink(ClientValue):
    Hits: Optional[int] = None
    NotFoundUrl: Optional[str] = None
    Referrers: ClientValueCollection[MissingLinkReferrer] = field(
        default_factory=lambda: ClientValueCollection(MissingLinkReferrer)
    )

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.SiteManager.MissingLink"

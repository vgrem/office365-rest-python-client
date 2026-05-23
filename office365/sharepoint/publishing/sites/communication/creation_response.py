from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.portal.sites.status import SiteStatus


@dataclass
class CommunicationSiteCreationResponse(ClientValue):
    SiteStatus: SiteStatus = SiteStatus.Unknown
    SiteUrl: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.CommunicationSiteCreationResponse"

from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.sharepoint.portal.sites.status import SiteStatus


@value
class CommunicationSiteCreationResponse(ClientValue):
    SiteStatus: SiteStatus = SiteStatus.Unknown
    SiteUrl: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.CommunicationSiteCreationResponse"

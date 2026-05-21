from dataclasses import dataclass
from typing import Any

from office365.runtime.client_value import ClientValue


@dataclass
class CommunicationSiteCreationResponse(ClientValue):
    SiteStatus: Any = None
    SiteUrl: Any = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.CommunicationSiteCreationResponse"

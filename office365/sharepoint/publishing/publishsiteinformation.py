from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class PublishSiteInformation(ClientValue):
    SiteType: Optional[int] = None
    SiteUrl: Optional[str] = None
    Title: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.PublishSiteInformation"

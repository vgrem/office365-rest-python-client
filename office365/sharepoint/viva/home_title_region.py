from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class VivaHomeTitleRegion(ClientValue):
    """Viva Home title region configuration.

    Fields:
        image_url (str):
    """

    ImageUrl: Optional[str] = None
    ListId: Optional[str] = None
    SiteId: Optional[str] = None
    TranslateX: Optional[float] = None
    TranslateY: Optional[float] = None
    UniqueId: Optional[str] = None
    WebId: Optional[str] = None

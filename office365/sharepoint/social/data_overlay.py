from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class SocialDataOverlay(ClientValue):
    """The SocialDataOverlay class provides information about an overlay. An overlay is a substring in a post that
    represents a user, document, site, tag, or link. The SocialPost class (see section 3.1.5.26) contains an array
     of SocialDataOverlay objects. Each of the SocialDataOverlay objects specifies a link or one or more actors."""

    ActorIndexes: ClientValueCollection[int] = field(default_factory=lambda: ClientValueCollection(int))
    Index: Optional[int] = None
    Length: Optional[int] = None
    LinkUri: Optional[str] = None
    OverlayType: Optional[int] = None

    @property
    def entity_type_name(self):
        return "SP.Social.SocialDataOverlay"

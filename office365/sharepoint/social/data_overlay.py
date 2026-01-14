from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


class SocialDataOverlay(ClientValue):
    def __init__(
        self,
        actor_indexes: ClientValueCollection[int] = ClientValueCollection(int),
        index: int = None,
        length: int = None,
        link_uri: str = None,
        overlay_type: int = None,
    ):
        """The SocialDataOverlay class provides information about an overlay. An overlay is a substring in a post that
        represents a user, document, site, tag, or link. The SocialPost class (see section 3.1.5.26) contains an array
         of SocialDataOverlay objects. Each of the SocialDataOverlay objects specifies a link or one or more actors.
        """
        self.ActorIndexes = actor_indexes
        self.Index = index
        self.Length = length
        self.LinkUri = link_uri
        self.OverlayType = overlay_type

    @property
    def entity_type_name(self):
        return "SP.Social.SocialDataOverlay"

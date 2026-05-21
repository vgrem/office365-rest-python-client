from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.social.thread import SocialThread


@dataclass
class SocialFeed(ClientValue):
    """
    The SocialFeed class specifies a feed, which contains an array of SocialThread (section 3.1.5.42), each of which
    specifies a root SocialPost object (section 3.1.5.26) and an array of response SocialPost objects.
    """

    Attributes: int | None = None
    NewestProcessed: str | None = None
    OldestProcessed: str | None = None
    Threads: ClientValueCollection[SocialThread] = field(default_factory=lambda: ClientValueCollection(SocialThread))
    UnreadMentionCount: int | None = None

    @property
    def entity_type_name(self):
        return "SP.Social.SocialFeed"

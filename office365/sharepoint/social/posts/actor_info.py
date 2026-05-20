from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class SocialPostActorInfo(ClientValue):
    """The SocialPostActorInfo class specifies a set of users, documents, sites, and tags by an index into the
    SocialThread Actors array (see section 3.1.5.42.1.1.1).
    In the SocialPost LikerInfo property (see section 3.1.5.26.1.1.6), this class represents a set of users that
    like the post."""

    IncludesCurrentUser: Optional[bool] = None
    Indexes: ClientValueCollection[int] = field(default_factory=lambda: ClientValueCollection(int))
    TotalCount: Optional[int] = None

    @property
    def entity_type_name(self):
        return "SP.Social.SocialPostActorInfo"

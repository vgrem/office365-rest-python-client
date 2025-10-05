from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


class SocialPostActorInfo(ClientValue):

    def __init__(
        self,
        includes_current_user: bool = None,
        indexes: ClientValueCollection[int] = ClientValueCollection(int),
        total_count: int = None,
    ):
        """The SocialPostActorInfo class specifies a set of users, documents, sites, and tags by an index into the
        SocialThread Actors array (see section 3.1.5.42.1.1.1).
        In the SocialPost LikerInfo property (see section 3.1.5.26.1.1.6), this class represents a set of users that
        like the post."""
        self.IncludesCurrentUser = includes_current_user
        self.Indexes = indexes
        self.TotalCount = total_count

    @property
    def entity_type_name(self):
        return "SP.Social.SocialPostActorInfo"

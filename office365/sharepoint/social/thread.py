from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.social.actor import SocialActor
from office365.sharepoint.social.posts.post import SocialPost
from office365.sharepoint.social.posts.reference import SocialPostReference


@dataclass
class SocialThread(ClientValue):
    """The SocialThread property provides the object that contains the thread.
    For details on the SocialThread type, see section 3.1.5.42."""

    Actors: ClientValueCollection[SocialActor] = field(default_factory=lambda: ClientValueCollection(SocialActor))
    RootPost: SocialPost = field(default_factory=SocialPost)
    Replies: ClientValueCollection[SocialPost] = field(default_factory=lambda: ClientValueCollection(SocialPost))
    PostReference: SocialPostReference = field(default_factory=SocialPostReference)
    Attributes: int | None = None
    Id: str | None = None
    OwnerIndex: int | None = None
    Permalink: str | None = None
    Status: int | None = None
    ThreadType: int | None = None
    TotalReplyCount: int | None = None

    @property
    def entity_type_name(self):
        return "SP.Social.SocialThread"

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class SocialActor(ClientValue):
    """The SocialActor type contains information about an actor retrieved from server. An actor is a user, document,
    site, or tag."""

    AccountName: Optional[str] = None
    ActorType: Optional[int] = None
    CanFollow: Optional[bool] = None
    ContentUri: Optional[str] = None
    EmailAddress: Optional[str] = None
    FollowedContentUri: Optional[str] = None
    GroupId: Optional[str] = None
    Id: Optional[str] = None
    ImageUri: Optional[str] = None
    IsFollowed: Optional[bool] = None
    LibraryUri: Optional[str] = None
    Name: Optional[str] = None
    PersonalSiteUri: Optional[str] = None
    Status: Optional[int] = None
    StatusText: Optional[str] = None
    TagGuid: Optional[str] = None
    Title: Optional[str] = None
    Uri: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Social.SocialActor"

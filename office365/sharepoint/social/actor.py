from typing import Optional

from office365.runtime.client_value import ClientValue


class SocialActor(ClientValue):
    def __init__(
        self,
        account_name: Optional[str] = None,
        actor_type: Optional[int] = None,
        can_follow: Optional[bool] = None,
        content_uri: Optional[str] = None,
        email_address: Optional[str] = None,
        followed_content_uri: Optional[str] = None,
        group_id: Optional[str] = None,
        id_: Optional[str] = None,
        image_uri: Optional[str] = None,
        is_followed: Optional[bool] = None,
        library_uri: Optional[str] = None,
        name: Optional[str] = None,
        personal_site_uri: Optional[str] = None,
        status: Optional[int] = None,
        status_text: Optional[str] = None,
        tag_guid: Optional[str] = None,
        title: Optional[str] = None,
        uri: Optional[str] = None,
    ):
        """The SocialActor type contains information about an actor retrieved from server. An actor is a user, document,
        site, or tag."""
        self.AccountName = account_name
        self.ActorType = actor_type
        self.CanFollow = can_follow
        self.ContentUri = content_uri
        self.EmailAddress = email_address
        self.FollowedContentUri = followed_content_uri
        self.GroupId = group_id
        self.Id = id_
        self.ImageUri = image_uri
        self.IsFollowed = is_followed
        self.LibraryUri = library_uri
        self.Name = name
        self.PersonalSiteUri = personal_site_uri
        self.Status = status
        self.StatusText = status_text
        self.TagGuid = tag_guid
        self.Title = title
        self.Uri = uri

    @property
    def entity_type_name(self):
        return "SP.Social.SocialActor"

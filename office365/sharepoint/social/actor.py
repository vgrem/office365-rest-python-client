from office365.runtime.client_value import ClientValue


class SocialActor(ClientValue):

    def __init__(
        self,
        account_name: str = None,
        actor_type: int = None,
        can_follow: bool = None,
        content_uri: str = None,
        email_address: str = None,
        followed_content_uri: str = None,
        group_id: str = None,
        id_: str = None,
        image_uri: str = None,
        is_followed: bool = None,
        library_uri: str = None,
        name: str = None,
        personal_site_uri: str = None,
        status: int = None,
        status_text: str = None,
        tag_guid: str = None,
        title: str = None,
        uri: str = None,
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

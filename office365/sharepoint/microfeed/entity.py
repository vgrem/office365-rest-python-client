from office365.runtime.client_value import ClientValue


class MicroBlogEntity(ClientValue):
    def __init__(
        self,
        account_name: str = None,
        can_follow: bool = None,
        description: str = None,
        display_name: str = None,
        email: str = None,
        entity_type: int = None,
        entity_uri: str = None,
        followed_content_uri: str = None,
        identifier: str = None,
        is_followed_by_me: bool = None,
        latest_post: str = None,
        library_name: str = None,
        library_uri: str = None,
        personal_uri: str = None,
        picture_uri: str = None,
        status: int = None,
        title: str = None,
    ):
        self.AccountName = account_name
        self.CanFollow = can_follow
        self.Description = description
        self.DisplayName = display_name
        self.Email = email
        self.EntityType = entity_type
        self.EntityURI = entity_uri
        self.FollowedContentURI = followed_content_uri
        self.Identifier = identifier
        self.IsFollowedByMe = is_followed_by_me
        self.LatestPost = latest_post
        self.LibraryName = library_name
        self.LibraryUri = library_uri
        self.PersonalURI = personal_uri
        self.PictureURI = picture_uri
        self.Status = status
        self.Title = title

    @property
    def entity_type_name(self):
        return "SP.Microfeed.MicroBlogEntity"

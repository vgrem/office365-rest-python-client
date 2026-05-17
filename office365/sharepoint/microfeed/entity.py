from typing import Optional

from office365.runtime.client_value import ClientValue


class MicroBlogEntity(ClientValue):
    def __init__(
        self,
        account_name: Optional[str] = None,
        can_follow: Optional[bool] = None,
        description: Optional[str] = None,
        display_name: Optional[str] = None,
        email: Optional[str] = None,
        entity_type: Optional[int] = None,
        entity_uri: Optional[str] = None,
        followed_content_uri: Optional[str] = None,
        identifier: Optional[str] = None,
        is_followed_by_me: Optional[bool] = None,
        latest_post: Optional[str] = None,
        library_name: Optional[str] = None,
        library_uri: Optional[str] = None,
        personal_uri: Optional[str] = None,
        picture_uri: Optional[str] = None,
        status: Optional[int] = None,
        title: Optional[str] = None,
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

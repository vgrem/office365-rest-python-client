from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.microfeed.link import MicrofeedLink


class MicrofeedPost(ClientValue):

    def __init__(
        self,
        author_index: int = None,
        bread_crumb: str = None,
        can_delete: bool = None,
        can_follow_up: bool = None,
        can_have_attachments: bool = None,
        can_like: bool = None,
        can_lock: bool = None,
        can_reply: bool = None,
        content: str = None,
        created: datetime = None,
        footer: str = None,
        id_: str = None,
        i_like_it: bool = None,
        likers_list: ClientValueCollection[int] = ClientValueCollection(int),
        locked: bool = None,
        media_link: MicrofeedLink = MicrofeedLink(),
        micro_blog_type: int = None,
        modified: datetime = None,
        people_count: int = None,
        post_image_uri: str = None,
        post_source: str = None,
        post_source_uri: str = None,
        reference_id: str = None,
        render_post_author_image: bool = None,
        reply_count: int = None,
        small_image_size_preferred: bool = None,
        title: str = None,
    ):
        self.AuthorIndex = author_index
        self.BreadCrumb = bread_crumb
        self.CanDelete = can_delete
        self.CanFollowUp = can_follow_up
        self.CanHaveAttachments = can_have_attachments
        self.CanLike = can_like
        self.CanLock = can_lock
        self.CanReply = can_reply
        self.Content = content
        self.Created = created
        self.Footer = footer
        self.ID = id_
        self.ILikeIt = i_like_it
        self.LikersList = likers_list
        self.Locked = locked
        self.MediaLink = media_link
        self.MicroBlogType = micro_blog_type
        self.Modified = modified
        self.PeopleCount = people_count
        self.PostImageUri = post_image_uri
        self.PostSource = post_source
        self.PostSourceUri = post_source_uri
        self.ReferenceID = reference_id
        self.RenderPostAuthorImage = render_post_author_image
        self.ReplyCount = reply_count
        self.SmallImageSizePreferred = small_image_size_preferred
        self.Title = title

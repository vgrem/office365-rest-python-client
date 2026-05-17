from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.microfeed.link import MicrofeedLink


class MicrofeedPost(ClientValue):
    def __init__(
        self,
        author_index: Optional[int] = None,
        bread_crumb: Optional[str] = None,
        can_delete: Optional[bool] = None,
        can_follow_up: Optional[bool] = None,
        can_have_attachments: Optional[bool] = None,
        can_like: Optional[bool] = None,
        can_lock: Optional[bool] = None,
        can_reply: Optional[bool] = None,
        content: Optional[str] = None,
        created: Optional[datetime] = None,
        footer: Optional[str] = None,
        id_: Optional[str] = None,
        i_like_it: Optional[bool] = None,
        likers_list: ClientValueCollection[int] = ClientValueCollection(int),
        locked: Optional[bool] = None,
        media_link: MicrofeedLink = MicrofeedLink(),
        micro_blog_type: Optional[int] = None,
        modified: Optional[datetime] = None,
        people_count: Optional[int] = None,
        post_image_uri: Optional[str] = None,
        post_source: Optional[str] = None,
        post_source_uri: Optional[str] = None,
        reference_id: Optional[str] = None,
        render_post_author_image: Optional[bool] = None,
        reply_count: Optional[int] = None,
        small_image_size_preferred: Optional[bool] = None,
        title: Optional[str] = None,
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

    @property
    def entity_type_name(self):
        return "SP.Microfeed.MicrofeedPost"

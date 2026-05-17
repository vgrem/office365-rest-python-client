from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.microfeed.datalink import MicrofeedDataLink
from office365.sharepoint.microfeed.entity import MicroBlogEntity
from office365.sharepoint.microfeed.posts.collection import MicrofeedPostCollection
from office365.sharepoint.microfeed.posts.post import MicrofeedPost


class MicrofeedThread(ClientValue):
    def __init__(
        self,
        can_follow_up: Optional[bool] = None,
        can_have_attachments: Optional[bool] = None,
        can_like: Optional[bool] = None,
        can_reply: Optional[bool] = None,
        data_links: ClientValueCollection[MicrofeedDataLink] = ClientValueCollection(MicrofeedDataLink),
        definition_id: Optional[int] = None,
        definition_name: Optional[str] = None,
        identifier: Optional[str] = None,
        locked: Optional[bool] = None,
        microfeed_entities: ClientValueCollection[MicroBlogEntity] = ClientValueCollection(MicroBlogEntity),
        owner_index: Optional[int] = None,
        ref_reply: MicrofeedPost = MicrofeedPost(),
        ref_root: MicrofeedPost = MicrofeedPost(),
        render_post_author_image: Optional[bool] = None,
        replies: MicrofeedPostCollection = MicrofeedPostCollection(),
        reply_count: Optional[int] = None,
        root_post: MicrofeedPost = MicrofeedPost(),
        small_image_size_preferred: Optional[bool] = None,
        status: Optional[int] = None,
    ):
        self.CanFollowUp = can_follow_up
        self.CanHaveAttachments = can_have_attachments
        self.CanLike = can_like
        self.CanReply = can_reply
        self.DataLinks = data_links
        self.DefinitionId = definition_id
        self.DefinitionName = definition_name
        self.Identifier = identifier
        self.Locked = locked
        self.MicrofeedEntities = microfeed_entities
        self.OwnerIndex = owner_index
        self.RefReply = ref_reply
        self.RefRoot = ref_root
        self.RenderPostAuthorImage = render_post_author_image
        self.Replies = replies
        self.ReplyCount = reply_count
        self.RootPost = root_post
        self.SmallImageSizePreferred = small_image_size_preferred
        self.Status = status

    @property
    def entity_type_name(self):
        return "SP.Microfeed.MicrofeedThread"

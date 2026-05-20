from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.microfeed.datalink import MicrofeedDataLink
from office365.sharepoint.microfeed.entity import MicroBlogEntity
from office365.sharepoint.microfeed.posts.collection import MicrofeedPostCollection
from office365.sharepoint.microfeed.posts.post import MicrofeedPost


@dataclass
class MicrofeedThread(ClientValue):
    CanFollowUp: Optional[bool] = None
    CanHaveAttachments: Optional[bool] = None
    CanLike: Optional[bool] = None
    CanReply: Optional[bool] = None
    DataLinks: ClientValueCollection[MicrofeedDataLink] = field(
        default_factory=lambda: ClientValueCollection(MicrofeedDataLink)
    )
    DefinitionId: Optional[int] = None
    DefinitionName: Optional[str] = None
    Identifier: Optional[str] = None
    Locked: Optional[bool] = None
    MicrofeedEntities: ClientValueCollection[MicroBlogEntity] = field(
        default_factory=lambda: ClientValueCollection(MicroBlogEntity)
    )
    OwnerIndex: Optional[int] = None
    RefReply: MicrofeedPost = field(default_factory=MicrofeedPost)
    RefRoot: MicrofeedPost = field(default_factory=MicrofeedPost)
    RenderPostAuthorImage: Optional[bool] = None
    Replies: MicrofeedPostCollection = field(default_factory=MicrofeedPostCollection)
    ReplyCount: Optional[int] = None
    RootPost: MicrofeedPost = field(default_factory=MicrofeedPost)
    SmallImageSizePreferred: Optional[bool] = None
    Status: Optional[int] = None

    @property
    def entity_type_name(self):
        return "SP.Microfeed.MicrofeedThread"

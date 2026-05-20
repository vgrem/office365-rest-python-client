from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.microfeed.link import MicrofeedLink


@dataclass
class MicrofeedPost(ClientValue):
    AuthorIndex: Optional[int] = None
    BreadCrumb: Optional[str] = None
    CanDelete: Optional[bool] = None
    CanFollowUp: Optional[bool] = None
    CanHaveAttachments: Optional[bool] = None
    CanLike: Optional[bool] = None
    CanLock: Optional[bool] = None
    CanReply: Optional[bool] = None
    Content: Optional[str] = None
    Created: Optional[datetime] = None
    Footer: Optional[str] = None
    ID: Optional[str] = None
    ILikeIt: Optional[bool] = None
    LikersList: ClientValueCollection[int] = field(default_factory=lambda: ClientValueCollection(int))
    Locked: Optional[bool] = None
    MediaLink: MicrofeedLink = field(default_factory=MicrofeedLink)
    MicroBlogType: Optional[int] = None
    Modified: Optional[datetime] = None
    PeopleCount: Optional[int] = None
    PostImageUri: Optional[str] = None
    PostSource: Optional[str] = None
    PostSourceUri: Optional[str] = None
    ReferenceID: Optional[str] = None
    RenderPostAuthorImage: Optional[bool] = None
    ReplyCount: Optional[int] = None
    SmallImageSizePreferred: Optional[bool] = None
    Title: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Microfeed.MicrofeedPost"

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class MicrofeedPostDefinition(ClientValue):
    CanDelete: Optional[bool] = None
    CanFollowUp: Optional[bool] = None
    CanHaveAttachments: Optional[bool] = None
    CanLike: Optional[bool] = None
    CanLock: Optional[bool] = None
    CanReply: Optional[bool] = None
    CreationTime: Optional[datetime] = None
    DefinitionId: Optional[int] = None
    DefinitionName: Optional[str] = None
    DefinitionVersion: Optional[int] = None
    EnablePeopleList: Optional[bool] = None
    IsDefault: Optional[bool] = None
    IsEnabled: Optional[bool] = None
    IsNotification: Optional[bool] = None
    IsPrivate: Optional[bool] = None
    IsUserPost: Optional[bool] = None
    LastUpdateTime: Optional[datetime] = None
    PartitionId: Optional[str] = None
    PersistToCache: Optional[bool] = None
    PersistToPrivateFolder: Optional[bool] = None
    PersistToPublishedFeed: Optional[bool] = None
    ReferenceLikePostName: Optional[str] = None
    ReferenceMentionPostName: Optional[str] = None
    ReferenceReplyPostName: Optional[str] = None
    RenderPostAuthorImage: Optional[bool] = None
    ResourceFileName: Optional[str] = None
    SecurityTrimContentUrl: Optional[bool] = None
    SmallImageSizePreferred: Optional[bool] = None

    @property
    def entity_type_name(self):
        return "SP.Microfeed.MicrofeedPostDefinition"

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.microfeed.datalinkcollection import (
    MicrofeedDataLinkCollection,
)
from office365.sharepoint.microfeed.link import MicrofeedLink


@dataclass
class MicrofeedPostOptions(ClientValue):
    Content: Optional[str] = None
    ContentFormattingOption: Optional[int] = None
    DataLinks: MicrofeedDataLinkCollection = field(default_factory=MicrofeedDataLinkCollection)
    DefinitionName: Optional[str] = None
    MediaLink: MicrofeedLink = field(default_factory=MicrofeedLink)
    PeopleList: StringCollection = field(default_factory=StringCollection)
    PostSource: Optional[str] = None
    PostSourceUri: Optional[str] = None
    RefThread_ReferenceID: Optional[str] = None
    RefThread_RefReply: Optional[str] = None
    RefThread_RefRoot: Optional[str] = None
    TargetActor: Optional[str] = None
    UpdateStatusText: Optional[bool] = None

    @property
    def entity_type_name(self):
        return "SP.Microfeed.MicrofeedPostOptions"

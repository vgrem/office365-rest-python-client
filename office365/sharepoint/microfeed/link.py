from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.microfeed.linkaction import MicrofeedLinkAction


@dataclass
class MicrofeedLink(ClientValue):
    ClickAction: MicrofeedLinkAction = field(default_factory=MicrofeedLinkAction)
    ContentUri: Optional[str] = None
    Description: Optional[str] = None
    Height: Optional[int] = None
    Href: Optional[str] = None
    Length: Optional[int] = None
    LinkType: Optional[int] = None
    Name: Optional[str] = None
    PreviewHeight: Optional[int] = None
    PreviewPictureUrl: Optional[str] = None
    PreviewWidth: Optional[int] = None
    Status: Optional[int] = None
    Width: Optional[int] = None

    @property
    def entity_type_name(self):
        return "SP.Microfeed.MicrofeedLink"

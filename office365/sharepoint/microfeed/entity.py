from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class MicroBlogEntity(ClientValue):
    AccountName: Optional[str] = None
    CanFollow: Optional[bool] = None
    Description: Optional[str] = None
    DisplayName: Optional[str] = None
    Email: Optional[str] = None
    EntityType: Optional[int] = None
    EntityURI: Optional[str] = None
    FollowedContentURI: Optional[str] = None
    Identifier: Optional[str] = None
    IsFollowedByMe: Optional[bool] = None
    LatestPost: Optional[str] = None
    LibraryName: Optional[str] = None
    LibraryUri: Optional[str] = None
    PersonalURI: Optional[str] = None
    PictureURI: Optional[str] = None
    Status: Optional[int] = None
    Title: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Microfeed.MicroBlogEntity"

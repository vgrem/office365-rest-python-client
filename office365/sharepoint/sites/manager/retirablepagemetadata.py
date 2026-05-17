from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


class RetirablePageMetadata(ClientValue):
    def __init__(
        self,
        description: Optional[str] = None,
        last_activity_timestamp: Optional[datetime] = None,
        path: Optional[str] = None,
        picture_thumbnail_url: Optional[str] = None,
        title: Optional[str] = None,
    ):
        self.Description = description
        self.LastActivityTimestamp = last_activity_timestamp
        self.Path = path
        self.PictureThumbnailUrl = picture_thumbnail_url
        self.Title = title

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.SiteManager.RetirablePageMetadata"

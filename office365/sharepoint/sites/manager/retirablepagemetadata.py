from datetime import datetime

from office365.runtime.client_value import ClientValue


class RetirablePageMetadata(ClientValue):
    def __init__(
        self,
        description: str = None,
        last_activity_timestamp: datetime = None,
        path: str = None,
        picture_thumbnail_url: str = None,
        title: str = None,
    ):
        self.Description = description
        self.LastActivityTimestamp = last_activity_timestamp
        self.Path = path
        self.PictureThumbnailUrl = picture_thumbnail_url
        self.Title = title

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.SiteManager.RetirablePageMetadata"

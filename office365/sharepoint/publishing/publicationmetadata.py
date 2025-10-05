from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.sharepoint.publishing.amplify.amplifiedchannels import AmplifiedChannels
from office365.sharepoint.sharepointids import SharePointIds


class PublicationMetadata(ClientValue):

    def __init__(
        self,
        amplified_channels: AmplifiedChannels = AmplifiedChannels(),
        banner_image_url: str = None,
        can_edit: bool = None,
        creation_date: datetime = None,
        id_: int = None,
        modified_date: datetime = None,
        share_point_ids: SharePointIds = SharePointIds(),
        status: str = None,
        title: str = None,
        url: str = None,
    ):
        self.AmplifiedChannels = amplified_channels
        self.BannerImageUrl = banner_image_url
        self.CanEdit = can_edit
        self.CreationDate = creation_date
        self.Id = id_
        self.ModifiedDate = modified_date
        self.SharePointIds = share_point_ids
        self.Status = status
        self.Title = title
        self.Url = url

from typing import Optional

from office365.runtime.client_value import ClientValue


class GettyImage(ClientValue):
    def __init__(
        self,
        image_id: Optional[str] = None,
        image_url: Optional[str] = None,
        insertion_iso_timestamp: Optional[str] = None,
        primary_id: Optional[str] = None,
        secondary_id: Optional[str] = None,
    ):
        self.ImageId = image_id
        self.ImageUrl = image_url
        self.InsertionISOTimestamp = insertion_iso_timestamp
        self.PrimaryId = primary_id
        self.SecondaryId = secondary_id

    @property
    def entity_type_name(self):
        return "SP.Publishing.GettyImage"

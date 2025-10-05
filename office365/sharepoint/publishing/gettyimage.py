from office365.runtime.client_value import ClientValue


class GettyImage(ClientValue):

    def __init__(
        self,
        image_id: str = None,
        image_url: str = None,
        insertion_iso_timestamp: str = None,
        primary_id: str = None,
        secondary_id: str = None,
    ):
        self.ImageId = image_id
        self.ImageUrl = image_url
        self.InsertionISOTimestamp = insertion_iso_timestamp
        self.PrimaryId = primary_id
        self.SecondaryId = secondary_id

    @property
    def entity_type_name(self):
        return "SP.Publishing.GettyImage"

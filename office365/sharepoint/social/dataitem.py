from office365.runtime.client_value import ClientValue


class SocialDataItem(ClientValue):
    def __init__(
        self,
        account_name: str = None,
        item_type: int = None,
        tag_guid: str = None,
        text: str = None,
        uri: str = None,
    ):
        self.AccountName = account_name
        self.ItemType = item_type
        self.TagGuid = tag_guid
        self.Text = text
        self.Uri = uri

    @property
    def entity_type_name(self):
        return "SP.Social.SocialDataItem"

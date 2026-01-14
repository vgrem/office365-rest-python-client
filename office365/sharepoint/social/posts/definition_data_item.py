from office365.runtime.client_value import ClientValue


class SocialPostDefinitionDataItem(ClientValue):
    def __init__(
        self,
        account_name: str = None,
        item_type: int = None,
        placeholder_name: str = None,
        tag_guid: str = None,
        text: str = None,
        uri: str = None,
    ):
        """The SocialPostDefinitionDataItem class specifies an item to be inserted in a post by replacing a token in
        the post definition. This type can only be specified in a server-to-server call.
        """
        self.AccountName = account_name
        self.ItemType = item_type
        self.PlaceholderName = placeholder_name
        self.TagGuid = tag_guid
        self.Text = text
        self.Uri = uri

    @property
    def entity_type_name(self):
        return "SP.Social.SocialPostDefinitionDataItem"

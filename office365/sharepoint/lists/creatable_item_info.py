from office365.runtime.client_value import ClientValue


class CreatableItemInfo(ClientValue):
    def __init__(
        self,
        document_template: int = None,
        file_extension: str = None,
        item_type: str = None,
    ):
        """
        Information on a creatable item: what the item is and where to go to create it. Alternatively, the information
        provided here can be used to call CreateDocument (section 3.2.5.79.2.2.9) or
        CreateDocumentAndGetEditLink (section 3.2.5.79.2.1.13)
        :param document_template:
        :param file_extension:
        :param item_type:
        """
        self.DocumentTemplate = document_template
        self.FileExtension = file_extension
        self.ItemType = item_type

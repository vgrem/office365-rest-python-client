from office365.runtime.client_value import ClientValue


class CreatableItemInfo(ClientValue):
    """
    Information on a creatable item: what the item is and where to go to create it. Alternatively, the information
    provided here can be used to call CreateDocument (section 3.2.5.79.2.2.9) or
    CreateDocumentAndGetEditLink (section 3.2.5.79.2.1.13).
    """

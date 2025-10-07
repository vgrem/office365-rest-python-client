from office365.runtime.client_value import ClientValue


class ContentTypeInfo(ClientValue):
    def __init__(self, id_: str = None, name: str = None):
        """
        The contentTypeInfo resource indicates the SharePoint content type of an item.

        :param str id_: The id of the content type.
        :param str name: The name of the content type.
        """
        self.id = id_
        self.name = name

from office365.runtime.client_value import ClientValue


class SerializableType(ClientValue):
    def __init__(self, type_: str = None):
        self.type = type_

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.News.DataModel.SerializableType"

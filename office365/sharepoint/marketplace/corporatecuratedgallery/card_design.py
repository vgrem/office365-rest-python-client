from office365.runtime.client_value import ClientValue


class CardDesign(ClientValue):

    def __init__(
        self,
        description: str = None,
        id_: str = None,
        serialized_properties: str = None,
        show_in_toolbox: bool = None,
        title: str = None,
    ):
        self.description = description
        self.id = id_
        self.serializedProperties = serialized_properties
        self.showInToolbox = show_in_toolbox
        self.title = title

    ""

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.CardDesign"

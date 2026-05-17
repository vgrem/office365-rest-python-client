from typing import Optional

from office365.runtime.client_value import ClientValue


class CardDesign(ClientValue):
    def __init__(
        self,
        description: Optional[str] = None,
        id_: Optional[str] = None,
        serialized_properties: Optional[str] = None,
        show_in_toolbox: Optional[bool] = None,
        title: Optional[str] = None,
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

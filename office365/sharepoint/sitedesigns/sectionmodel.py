from dataclasses import field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sitedesigns.webpartmodel import WebPartModel


class SectionModel(ClientValue):
    index: Optional[int] = None
    webParts: ClientValueCollection[WebPartModel] = field(default_factory=lambda: ClientValueCollection(WebPartModel))

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.SectionDesignIdeas.SectionModel"

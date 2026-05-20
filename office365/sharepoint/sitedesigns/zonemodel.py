from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sitedesigns.sectionmodel import SectionModel


@dataclass
class ZoneModel(ClientValue):
    index: Optional[int] = None
    sections: ClientValueCollection[SectionModel] = field(default_factory=lambda: ClientValueCollection(SectionModel))

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.SectionDesignIdeas.ZoneModel"

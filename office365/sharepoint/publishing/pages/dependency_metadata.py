from dataclasses import dataclass, field
from typing import Any, Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.webpartdetailswrapper import WebPartDetailsWrapper


@dataclass
class SitePageDependencyMetadata(ClientValue):
    DependencyItemPath: Any = None
    IsInPageSiteAssetsFolder: Any = None
    ListId: Any = None
    RelatedWebParts: Any = None
    SiteId: Any = None
    RelatedWebPartsDetails: ClientValueCollection[WebPartDetailsWrapper] = field(
        default_factory=lambda: ClientValueCollection(WebPartDetailsWrapper)
    )
    Type: Optional[str] = None
    UniqueId: Optional[str] = None
    WebId: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.SitePageDependencyMetadata"

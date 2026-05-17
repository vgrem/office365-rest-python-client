from office365.sharepoint.sitedesigns.creation_info import SiteDesignCreationInfo
from typing import Optional


class SiteDesignMetadata(SiteDesignCreationInfo):
    def __init__(self, order=None, version=None, id_: Optional[str] = None):
        super().__init__()
        self.Order = order
        self.Version = version
        self.Id = id_

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Utilities.WebTemplateExtensions.SiteDesignMetadata"

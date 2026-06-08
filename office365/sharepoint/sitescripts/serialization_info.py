from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class SiteScriptSerializationInfo(ClientValue):
    """Args:
        include_branding (bool):
        included_lists (list[str]):
        include_site_external_sharing_capability (bool):
        include_theme (bool):
    """

    IncludeBranding: Optional[bool] = None
    IncludedLists: Optional[StringCollection] = None
    IncludeLinksToExportedItems: Optional[bool] = None
    IncludeRegionalSettings: Optional[bool] = None
    IncludeSiteExternalSharingCapability: Optional[bool] = None
    IncludeTheme: Optional[bool] = None
    IncludedPages: Optional[StringCollection] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Utilities.WebTemplateExtensions.SiteScriptSerializationInfo"

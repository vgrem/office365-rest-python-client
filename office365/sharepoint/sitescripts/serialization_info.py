from __future__ import annotations

from typing import Optional


from dataclasses import dataclass
from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class SiteScriptSerializationInfo(ClientValue):

    """
    :param bool include_branding:
    :param list[str] included_lists:
    :param bool include_site_external_sharing_capability:
    :param bool include_theme:
    """

    IncludeBranding = None
    IncludedLists: StringCollection | None = None
    IncludeLinksToExportedItems = None
    IncludeRegionalSettings = None
    IncludeSiteExternalSharingCapability = None
    IncludeTheme = None
    IncludedPages: Optional[StringCollection] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Utilities.WebTemplateExtensions.SiteScriptSerializationInfo"
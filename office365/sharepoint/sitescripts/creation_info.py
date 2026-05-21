

from __future__ import annotations
from typing import Optional

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SiteScriptCreationInfo(ClientValue):

    Content: Optional[str] = None
    Description: Optional[str] = None
    Title: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Utilities.WebTemplateExtensions.SiteScriptCreationInfo"

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class MissingLinkReferrer(ClientValue):
    Title: Optional[str] = None
    Url: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.SiteManager.MissingLinkReferrer"

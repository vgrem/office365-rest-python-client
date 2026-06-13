from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class ScanForMissingLinksTaskResult(ClientValue):
    MissingLinks: StringCollection = field(default_factory=StringCollection)

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.SiteManager.ScanForMissingLinksTaskResult"

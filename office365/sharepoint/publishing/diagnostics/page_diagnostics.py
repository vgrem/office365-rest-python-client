from dataclasses import dataclass
from typing import Any, Optional

from office365.runtime.client_value import ClientValue


@dataclass
class PageDiagnostics(ClientValue):
    Results: Any = None
    LatestDraftVersion: Optional[str] = None
    LatestPublishedVersion: Optional[str] = None
    PageFileName: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Publishing.Diagnostics.PageDiagnostics"

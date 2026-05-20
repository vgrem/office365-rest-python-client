from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class OrgLabelsContext(ClientValue):
    DisplayName: Optional[str] = None
    LabelApplicableTo: Optional[str] = None
    ObjectId: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.OrgLabelsContext"

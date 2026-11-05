from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue


class OrgLabelsContext(ClientValue):
    DisplayName: Optional[str] = None
    LabelApplicableTo: Optional[str] = None
    ObjectId: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.OrgLabelsContext"

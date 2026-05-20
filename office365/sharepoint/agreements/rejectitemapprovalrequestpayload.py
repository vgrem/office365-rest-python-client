from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class RejectItemApprovalRequestPayload(ClientValue):
    approvalId: Optional[str] = None
    comments: Optional[str] = None
    itemId: Optional[str] = None
    url: Optional[str] = None
    version: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Agreements.Models.RejectItemApprovalRequestPayload"

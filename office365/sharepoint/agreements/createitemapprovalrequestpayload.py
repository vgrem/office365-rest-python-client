from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class CreateItemApprovalRequestPayload(ClientValue):
    approvalConfig: Optional[str] = None
    restrictDocEdit: Optional[bool] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Agreements.Models.CreateItemApprovalRequestPayload"

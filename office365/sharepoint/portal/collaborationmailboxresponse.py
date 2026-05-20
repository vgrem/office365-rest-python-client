from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class CollaborationMailboxResponse(ClientValue):
    AlternateUrl: Optional[str] = None
    CorrelationId: Optional[str] = None
    ErrorCode: Optional[int] = None
    Status: Optional[int] = None
    Url: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.CollaborationMailboxResponse"

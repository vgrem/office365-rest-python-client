from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class ApprovalsProperties(ClientValue):
    ApproversAwaitAll: Optional[bool] = None
    ApproversAwaitAllFixed: Optional[bool] = None
    ApproversFixed: Optional[bool] = None
    ApproverSourceType: Optional[int] = None
    ApproverSourceValue: Optional[str] = None
    ProvisioningError: Optional[str] = None
    ProvisioningStatus: Optional[int] = None
    NotificationsEnabled: Optional[bool] = None

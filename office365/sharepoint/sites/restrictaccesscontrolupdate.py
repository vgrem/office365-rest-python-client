from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class RestrictAccessControlUpdate(ClientValue):
    EnableRestrictedAccessPolicy: Optional[bool] = None
    Justification: Optional[str] = None
    RestrictedAccessControlGroups: StringCollection = field(default_factory=StringCollection)
    IsPolicyEnabledAtSite: Optional[bool] = None
    IsPolicyEnabledAtTenant: Optional[bool] = None
    AllowSharingOutsideRAC: Optional[bool] = None

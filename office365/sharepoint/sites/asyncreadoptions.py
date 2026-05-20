from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class AsyncReadOptions(ClientValue):
    IncludeDirectDescendantsOnly: Optional[bool] = None
    IncludeExtendedMetadata: Optional[bool] = None
    IncludePermission: Optional[bool] = None
    IncludeSecurity: Optional[bool] = None
    IncludeVersions: Optional[bool] = None
    StartChangeToken: Optional[str] = None

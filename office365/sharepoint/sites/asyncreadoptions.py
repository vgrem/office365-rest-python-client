from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class AsyncReadOptions(ClientValue):
    IncludeDirectDescendantsOnly: Optional[bool] = None
    IncludeExtendedMetadata: Optional[bool] = None
    IncludePermission: Optional[bool] = None
    IncludeSecurity: Optional[bool] = None
    IncludeVersions: Optional[bool] = None
    StartChangeToken: Optional[str] = None

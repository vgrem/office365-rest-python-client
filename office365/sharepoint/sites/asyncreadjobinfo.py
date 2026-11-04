from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class AsyncReadJobInfo(ClientValue):
    CurrentChangeToken: Optional[str] = None
    JobId: Optional[str] = None

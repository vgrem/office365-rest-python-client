from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class AsyncReadJobInfo(ClientValue):
    CurrentChangeToken: Optional[str] = None
    JobId: Optional[str] = None

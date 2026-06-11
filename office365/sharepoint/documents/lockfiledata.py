from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from office365.runtime.client_value import ClientValue


@dataclass
class LockFileData(ClientValue):
    lockExpireTimeStamp: datetime | None = field(default_factory=lambda: datetime.min)
    lockId: str | None = None

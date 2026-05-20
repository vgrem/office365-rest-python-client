from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class LockFileData(ClientValue):
    lock_expire_time_stamp: datetime = field(default_factory=lambda: datetime.min)
    lock_id: Optional[str] = None

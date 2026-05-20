from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class CoAuthConfiguration(ClientValue):
    source_session_id: Optional[str] = None
    update_date: datetime = field(default_factory=lambda: datetime.min)
    update_reason: Optional[int] = None

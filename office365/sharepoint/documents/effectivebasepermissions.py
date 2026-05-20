from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class EffectiveBasePermissions(ClientValue):
    High: Optional[str] = None
    Low: Optional[str] = None

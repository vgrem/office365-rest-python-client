from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class HomeSiteNavConfiguration(ClientValue):
    is_enabled: Optional[bool] = None
    logo_hash: Optional[str] = None

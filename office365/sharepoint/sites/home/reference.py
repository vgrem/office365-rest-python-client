from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import GuidCollection


@dataclass
class HomeSiteReference(ClientValue):
    audiences: GuidCollection = field(default_factory=GuidCollection)
    site_flags: Optional[int] = None
    site_id: Optional[str] = None
    web_id: Optional[str] = None

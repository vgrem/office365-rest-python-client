from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class SmartTemplateContentType(ClientValue):
    id: Optional[str] = None
    name: Optional[str] = None
    publish_status: Optional[str] = None

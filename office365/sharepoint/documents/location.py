from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class DocumentLocation(ClientValue):
    folder_id: Optional[int] = None
    library_id: Optional[str] = None
    site_id: Optional[str] = None
    web_id: Optional[str] = None

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class PortalAndOrgNewsSiteReference(ClientValue):
    is_in_draft_mode: Optional[bool] = None
    is_viva_backend: Optional[bool] = None
    site_id: Optional[str] = None
    web_id: Optional[str] = None

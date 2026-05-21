from __future__ import annotations

from typing import List, Optional


from dataclasses import dataclass
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sharing.audience import Audience


@dataclass
class TargetedSiteDetails(ClientValue):

    audiences: ClientValueCollection[Audience] | None = None
    is_in_draft_mode: Optional[bool] = None
    is_viva_backend_site: Optional[bool] = None
    site_id: Optional[str] = None
    targeted_license_type: Optional[int] = None
    title: Optional[str] = None
    url: Optional[str] = None
    viva_connections_default_start: Optional[bool] = None
    web_id: Optional[str] = None
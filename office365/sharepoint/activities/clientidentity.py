from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class ActivityClientIdentity(ClientValue):
    email: Optional[str] = None
    name: Optional[str] = None
    id: Optional[str] = None
    provider: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Activities.ActivityClientIdentity"

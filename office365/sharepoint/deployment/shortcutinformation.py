from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class ShortcutInformation(ClientValue):
    AddedById: Optional[int] = None
    Id: Optional[str] = None
    Name: Optional[str] = None
    Scenario: Optional[int] = None
    TimeCreated: Optional[datetime] = None
    TimeLastModified: Optional[datetime] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Deployment.ShortcutInformation"

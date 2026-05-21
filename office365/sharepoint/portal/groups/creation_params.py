from __future__ import annotations

from typing import Optional

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class GroupCreationParams(ClientValue):
    """Group creation params"""

    Classification: str = ""
    Description: str = ""
    CreationOptions: StringCollection = field(
        default_factory=lambda: StringCollection(["SPSiteLanguage:1033"])
    )
    Owners: StringCollection = field(default_factory=StringCollection)
    PreferredDataLocation: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.GroupCreationParams"

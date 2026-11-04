from __future__ import annotations

from dataclasses import field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.value import value


@value
class GroupCreationParams(ClientValue):
    """Group creation params"""

    Classification: str = ""
    Description: str = ""
    CreationOptions: StringCollection = field(default_factory=lambda: StringCollection(["SPSiteLanguage:1033"]))
    Owners: StringCollection = field(default_factory=StringCollection)
    PreferredDataLocation: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.GroupCreationParams"

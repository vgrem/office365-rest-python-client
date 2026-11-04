from dataclasses import field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.value import value


@value
class TeamAppInfo(ClientValue):
    Children: StringCollection = field(default_factory=StringCollection)
    Name: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Utilities.WebTemplateExtensions.TeamAppInfo"

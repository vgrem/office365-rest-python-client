from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class ToolDetails(ClientValue):
    Name: Optional[str] = None
    Version: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Publishing.Diagnostics.ToolDetails"

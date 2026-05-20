from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class CopilotFileUserRelationship(ClientValue):
    LastAccessDateTime: Optional[datetime] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Copilot.CopilotFileUserRelationship"

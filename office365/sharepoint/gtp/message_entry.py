from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class MessageEntry(ClientValue):
    """content: str"""

    content: Optional[str] = None
    Role: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Internal.MessageEntry"

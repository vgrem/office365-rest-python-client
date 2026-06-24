from dataclasses import field
from datetime import datetime

from office365.runtime.client_value import ClientValue


class ChatViewpoint(ClientValue):
    isHidden: bool | None = None
    lastMessageReadDateTime: datetime | None = field(default_factory=lambda: datetime.min)
    ""

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ChatViewpoint"

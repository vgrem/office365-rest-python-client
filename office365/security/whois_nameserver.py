from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from office365.runtime.client_value import ClientValue

if TYPE_CHECKING:
    from office365.security.threatintelligence.host import Host


class WhoisNameserver(ClientValue):
    firstSeenDateTime: datetime | None = None
    lastSeenDateTime: datetime | None = None
    host: Host | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.WhoisNameserver"

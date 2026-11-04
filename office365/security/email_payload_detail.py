from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class EmailPayloadDetail(ClientValue):
    fromEmail: str | None = None
    fromName: str | None = None
    isExternalSender: bool | None = None
    subject: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.EmailPayloadDetail"

from __future__ import annotations

from office365.security.attacksimulations.payload_detail import PayloadDetail


class EmailPayloadDetail(PayloadDetail):
    fromEmail: str | None = None
    fromName: str | None = None
    isExternalSender: bool | None = None
    subject: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.EmailPayloadDetail"

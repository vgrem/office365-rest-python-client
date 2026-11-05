from __future__ import annotations

from office365.runtime.client_value import ClientValue


class EmailSettings(ClientValue):
    senderDomain: str | None = None
    useCompanyBranding: bool | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.EmailSettings"

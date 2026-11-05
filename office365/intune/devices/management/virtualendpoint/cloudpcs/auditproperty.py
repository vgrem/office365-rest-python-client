from __future__ import annotations

from office365.runtime.client_value import ClientValue


class CloudPcAuditProperty(ClientValue):
    displayName: str | None = None
    newValue: str | None = None
    oldValue: str | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.CloudPcAuditProperty"

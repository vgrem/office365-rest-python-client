from __future__ import annotations

from office365.runtime.client_value import ClientValue


class LicenseProcessingState(ClientValue):
    state: str | None = None

    ""

    @property
    def entity_type_name(self):
        return "microsoft.graph.LicenseProcessingState"

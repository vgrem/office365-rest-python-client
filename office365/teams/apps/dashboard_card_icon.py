from __future__ import annotations

from office365.runtime.client_value import ClientValue


class TeamsAppDashboardCardIcon(ClientValue):
    iconUrl: str | None = None
    officeUIFabricIconName: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TeamsAppDashboardCardIcon"

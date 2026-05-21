from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.tenant.administration.powerapps.environment_context import (
    PowerAppsEnvironmentContext,
)


@dataclass
class SyntexPowerAppsEnvironmentsContext(ClientValue):
    Environments: ClientValueCollection[PowerAppsEnvironmentContext] = field(
        default_factory=lambda: ClientValueCollection(PowerAppsEnvironmentContext)
    )
    TimerJobSyncDisabled: bool | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SyntexPowerAppsEnvironmentsContext"

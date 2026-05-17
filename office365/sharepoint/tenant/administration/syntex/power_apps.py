from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.tenant.administration.powerapps.environment_context import (
    PowerAppsEnvironmentContext,
)


class SyntexPowerAppsEnvironmentsContext(ClientValue):
    """ """

    def __init__(self, environments=None, timer_job_sync_disabled=None):
        self.Environments = ClientValueCollection(PowerAppsEnvironmentContext, environments)
        self.TimerJobSyncDisabled = timer_job_sync_disabled

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SyntexPowerAppsEnvironmentsContext"

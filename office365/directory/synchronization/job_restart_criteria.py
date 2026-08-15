from office365.directory.synchronization.jobrestartscope import SynchronizationJobRestartScope
from office365.runtime.client_value import ClientValue


class SynchronizationJobRestartCriteria(ClientValue):
    resetScope: SynchronizationJobRestartScope = SynchronizationJobRestartScope.None_
    "Defines the scope of the synchronizationJob: restart action."

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SynchronizationJobRestartCriteria"

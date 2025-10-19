from enum import Enum


class SynchronizationJobRestartScope(Enum):
    None_ = "0"
    ConnectorDataStore = "1"
    Escrows = "2"
    Watermark = "4"
    QuarantineState = "8"
    Full = "15"
    ForceDeletes = "32"

    @property
    def entity_type_name(self):
        return "microsoft.graph.SynchronizationJobRestartScope"

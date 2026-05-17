from enum import Enum


class PersistentBrowserSessionMode(Enum):
    always = "0"
    never = "1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.PersistentBrowserSessionMode"

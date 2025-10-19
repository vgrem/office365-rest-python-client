from enum import Enum


class WindowsArchitecture(Enum):
    none = "0"
    x86 = "1"
    x64 = "2"
    arm = "4"
    neutral = "8"

    @property
    def entity_type_name(self):
        return "microsoft.graph.WindowsArchitecture"

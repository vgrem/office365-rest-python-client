from enum import Enum


class MdmAuthority(Enum):
    unknown = "0"
    intune = "1"
    sccm = "2"
    office365 = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.MdmAuthority"

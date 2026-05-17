from enum import Enum


class PhoneType(Enum):
    home = "0"
    business = "1"
    mobile = "2"
    other = "3"
    assistant = "4"
    homeFax = "5"
    businessFax = "6"
    otherFax = "7"
    pager = "8"
    radio = "9"

    none = "-1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.PhoneType"

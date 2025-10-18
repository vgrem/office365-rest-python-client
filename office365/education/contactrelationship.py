from enum import Enum


class ContactRelationship(Enum):
    parent = "0"
    relative = "1"
    aide = "2"
    doctor = "3"
    guardian = "4"
    child = "5"
    other = "6"
    unknownFutureValue = "7"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ContactRelationship"

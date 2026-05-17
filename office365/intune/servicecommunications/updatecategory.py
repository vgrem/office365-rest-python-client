from enum import Enum


class ServiceUpdateCategory(Enum):
    preventOrFixIssue = "1"
    planForChange = "2"
    stayInformed = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ServiceUpdateCategory"

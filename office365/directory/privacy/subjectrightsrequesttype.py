from enum import Enum


class SubjectRightsRequestType(Enum):
    export = "0"
    delete = "1"
    access = "2"
    tagForAction = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.SubjectRightsRequestType"

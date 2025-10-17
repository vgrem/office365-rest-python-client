from enum import Enum


class AccessPackageRequestType(Enum):
    notSpecified = "0"
    userAdd = "1"
    userUpdate = "2"
    userRemove = "3"
    adminAdd = "4"
    adminUpdate = "5"
    adminRemove = "6"
    systemAdd = "7"
    systemUpdate = "8"
    systemRemove = "9"
    onBehalfAdd = "10"
    unknownFutureValue = "11"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AccessPackageRequestType"

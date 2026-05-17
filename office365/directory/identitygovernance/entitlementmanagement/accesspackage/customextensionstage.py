from enum import Enum


class AccessPackageCustomExtensionStage(Enum):
    assignmentRequestCreated = "1"
    assignmentRequestApproved = "2"
    assignmentRequestGranted = "3"
    assignmentRequestRemoved = "4"
    assignmentFourteenDaysBeforeExpiration = "5"
    assignmentOneDayBeforeExpiration = "6"
    unknownFutureValue = "7"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AccessPackageCustomExtensionStage"

from enum import Enum


class CloudPcAuditActivityResult(Enum):
    success = "0"
    clientError = "1"
    failure = "2"
    timeout = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.CloudPcAuditActivityResult"

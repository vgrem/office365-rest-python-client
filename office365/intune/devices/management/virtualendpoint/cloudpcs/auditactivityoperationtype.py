from enum import Enum


class CloudPcAuditActivityOperationType(Enum):
    create = "0"
    delete = "1"
    patch = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.CloudPcAuditActivityOperationType"

from enum import Enum


class CloudPcAuditCategory(Enum):
    cloudPC = "0"
    unknownFutureValue = "1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.CloudPcAuditCategory"

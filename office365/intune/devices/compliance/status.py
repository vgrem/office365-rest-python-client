from enum import Enum


class ComplianceStatus(Enum):
    unknown = "0"
    notApplicable = "1"
    compliant = "2"
    remediated = "3"
    nonCompliant = "4"
    error = "5"
    conflict = "6"
    notAssigned = "7"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ComplianceStatus"

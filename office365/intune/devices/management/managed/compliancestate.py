from enum import Enum


class ComplianceState(Enum):
    unknown = "0"
    compliant = "1"
    noncompliant = "2"
    conflict = "3"
    error = "4"
    inGracePeriod = "254"
    configManager = "255"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ComplianceState"

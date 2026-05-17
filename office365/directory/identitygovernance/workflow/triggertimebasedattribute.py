from enum import Enum


class WorkflowTriggerTimeBasedAttribute(Enum):
    employeeHireDate = "0"
    employeeLeaveDateTime = "1"
    unknownFutureValue = "2"
    createdDateTime = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.identityGovernance.WorkflowTriggerTimeBasedAttribute"

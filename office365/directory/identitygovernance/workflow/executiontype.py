from enum import Enum


class WorkflowExecutionType(Enum):
    scheduled = "0"
    onDemand = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.identityGovernance.WorkflowExecutionType"

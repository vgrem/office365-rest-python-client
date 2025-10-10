from office365.directory.identitygovernance.workflow.triggertimebasedattribute import (
    WorkflowTriggerTimeBasedAttribute,
)
from office365.runtime.client_value import ClientValue


class TimeBasedAttributeTrigger(ClientValue):

    def __init__(
        self,
        offset_in_days: int = None,
        time_based_attribute: WorkflowTriggerTimeBasedAttribute = None,
    ):
        self.offsetInDays = offset_in_days
        self.timeBasedAttribute = time_based_attribute

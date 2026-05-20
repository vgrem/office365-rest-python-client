from __future__ import annotations

from dataclasses import dataclass

from office365.directory.identitygovernance.workflow.triggertimebasedattribute import WorkflowTriggerTimeBasedAttribute
from office365.runtime.client_value import ClientValue


@dataclass
class TimeBasedAttributeTrigger(ClientValue):
    offsetInDays: int | None = None
    timeBasedAttribute: WorkflowTriggerTimeBasedAttribute | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.identityGovernance.TimeBasedAttributeTrigger"

from dataclasses import field

from office365.directory.identitygovernance.workflow.executionconditions import WorkflowExecutionConditions
from office365.directory.identitygovernance.workflow.executiontrigger import WorkflowExecutionTrigger
from office365.directory.subjectset import SubjectSet


class TriggerAndScopeBasedConditions(WorkflowExecutionConditions):
    scope: SubjectSet = field(default_factory=SubjectSet)
    trigger: WorkflowExecutionTrigger = field(default_factory=WorkflowExecutionTrigger)

    @property
    def entity_type_name(self):
        return "microsoft.graph.identityGovernance.TriggerAndScopeBasedConditions"

from office365.directory.identitygovernance.workflow.executionconditions import WorkflowExecutionConditions
from office365.directory.identitygovernance.workflow.executiontrigger import WorkflowExecutionTrigger
from office365.directory.subjectset import SubjectSet


class TriggerAndScopeBasedConditions(WorkflowExecutionConditions):
    scope: SubjectSet = SubjectSet()
    trigger: WorkflowExecutionTrigger = WorkflowExecutionTrigger()

    @property
    def entity_type_name(self):
        return "microsoft.graph.identityGovernance.TriggerAndScopeBasedConditions"

from office365.directory.identitygovernance.workflow.executionconditions import WorkflowExecutionConditions
from office365.directory.identitygovernance.workflow.executiontrigger import WorkflowExecutionTrigger
from office365.directory.subjectset import SubjectSet


class TriggerAndScopeBasedConditions(WorkflowExecutionConditions):

    def __init__(self, scope=SubjectSet(), trigger=WorkflowExecutionTrigger()):
        self.scope = scope
        self.trigger = trigger

    @property
    def entity_type_name(self):
        return "microsoft.graph.identityGovernance.TriggerAndScopeBasedConditions"
